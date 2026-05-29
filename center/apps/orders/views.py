from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from .shop_cart import ShopCart
from apps.products.models import Product
from django.http import HttpResponse,JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.orders.models import Customer
from .models import Order,OrderDetails,PaymentType
from .forms import OrderForm
from django.core.exceptions import ObjectDoesNotExist
from apps.discounts.forms import CouponForm
from apps.discounts.models import Coupon
from django.db.models import Q
from datetime import datetime
from django.contrib import messages
import utils
from django.urls import reverse

# ______________________________________________________________________________________
class ShopCartView(View):
    def get(self, request, *args, **kwargs):
        shop_cart = ShopCart(request)
        total_price = shop_cart.calc_total_price()
        order_final_price, delivery, tax = utils.price_by_delivery_tax(total_price)

        context = {  # همه متغیرها
            'shop_cart': shop_cart,
            'total_price': total_price,
            'delivery': delivery,
            'tax': tax,
            'order_final_price': order_final_price
        }
        return render(request, 'orders_app/shop_cart.html', context)

# ______________________________________________________________________________________
def show_shop_cart(request):
    shop_cart=ShopCart(request)
    total_price=shop_cart.calc_total_price()
    order_final_price,delivery,tax=utils.price_by_delivery_tax(total_price)
    context={
        'shop_cart':shop_cart,
        'shop_cart_count':shop_cart.count,
        'total_price':total_price,
        'delivery':delivery,
        'tax':tax,
        'order_final_price':order_final_price
        }
    return render(request, 'orders_app/partials/show_shop_cart.html',context)

# ______________________________________________________________________________________
from django.http import JsonResponse
def add_to_shop_cart(request):
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return HttpResponse("فقط درخواست AJAX مجاز است", status=400)
    product_id = request.GET.get('product_id')
    quantity = request.GET.get('qty')
    shop_cart = ShopCart(request)
    product = get_object_or_404(Product, id=product_id)
    shop_cart.add_to_shop_cart(product, quantity)
    return JsonResponse({
        'count': shop_cart.count,
        'message': 'کالا به سبد خرید اضافه شد'
    })

# ______________________________________________________________________________________
def delete_from_shop_cart(request):
    product_id = request.GET.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    shop_cart = ShopCart(request)
    shop_cart.delete_from_shop_cart(product)
    return redirect('orders:show_shop_cart')

# ______________________________________________________________________________________
def update_shop_cart(request):
    product_id_list = request.GET.getlist('product_id_list[]')  # هر وقت از سمت جاوا اسکریپت یه لیستی رو میگیریم حتما باید آحرش اینجا یه [] بزاریم
    qty_list = request.GET.getlist('qty_list[]')
    shop_cart = ShopCart(request)
    shop_cart.update(product_id_list, qty_list)
    return redirect('orders:shop_cart')

# ______________________________________________________________________________________
def status_of_shop_cart(request):
    shop_cart = ShopCart(request)
    return JsonResponse({
        'count': shop_cart.count
    })

# ______________________________________________________________________________________
# وقتی دکمه ادامه خرید کلیک شد اول چک کنه اگه کاربر لاگ این نیست اول لاگ این کنه و بعد سفارش رو انجام بده
# رو ایمپورت کنم LoginRequiredMixin برای اینکار باید
class CreateOrderView(LoginRequiredMixin, View):
    def get(self, request):

        # 1 خواندن سبد خرید
        shop_cart = ShopCart(request)
        if len(shop_cart) == 0:
            return redirect('orders:shop_cart')  # اگر سبد خالی است، برگرد به صفحه سبد خرید

        # 2 Customer یافتن یا ساخت
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            customer = Customer.objects.create(user=request.user)

        # 3 ساخت سفارش جدید
        order = Order.objects.create(
            customer=customer,
            payment_type=get_object_or_404(PaymentType, id=1)  # دیفالت درگاه بانکی
        )

        # 4 OrderDetails انتقال آیتم‌ها از سبد به
        for item in shop_cart:
            OrderDetails.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['final_price'],
            )

        return redirect('orders:checkout_order', order.id)

# ______________________________________________________________________________________
#  استفاده میکنم LoginRequiredMixin تو قسمت ادامه خرید هم حتما کاربر باید لاگ این کرده باشه به همین دلیل باز هم از
class CheckOutView(LoginRequiredMixin,View):
    def get(self, request, order_id):
        user=request.user  # اول اینکه ببینم یوزر کیه
        customer=get_object_or_404(Customer, user=user)
        shop_cart=ShopCart(request)
        order=get_object_or_404(Order, id=order_id, customer__user=request.user) # اینطوری فقط صاحب سفارش می‌تونه واردش بشه دیگه هرکی اوردر آی دی داشته باشه نمیتونه وارد شه

        total_price=shop_cart.calc_total_price()
        order_final_price,delivery,tax=utils.price_by_delivery_tax(total_price,order.discount)  # تخفیف رو از قیمت نهایی کم کن

        # بصورت اختیاری این دیکشنری برای اینه که وقتی تو دیتا بیس فیلدی رو پر کنی تو وب اون اطلاعات پر شده درون فرم های مرحله جزئیات سفارش(سفارش شما) رو نشون بده
        data={
            'name': user.name,
            'family': user.family,
            'email': user.email,
            'phone_number': customer.phone_number,
            'address': customer.address,
            'description': order.description,
            'payment_type': order.payment_type.id if order.payment_type else None

        }

        form=OrderForm(data)
        form_coupon=CouponForm()
        context={
            'shop_cart':shop_cart,
            'total_price':total_price,
            'delivery':delivery,
            'tax':tax,
            'order_final_price':order_final_price,
            'order':order,
            'form':form,
            'form_coupon':form_coupon
        }
        return render(request, 'orders_app/checkout.html',context)

    # تابع پست برای زدن دکمه ثبت سفارش
    def post(self, request, order_id):
        print(">>> Checkout POST called")
        form=OrderForm(request.POST)
        print("POST DATA:", request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            try:
                order=Order.objects.get(id=order_id)
                print(">>> Order fetched:", order)
                order.description=cd['description']
                order.payment_type = cd['payment_type']
                order.save()

                user=request.user  # لاگ این شده یعنی آنلاینه یوزر رو بگیر LoginRequiredMixin این یوزر هم قبلا به وسیله
                user.name=cd['name']
                user.family=cd['family']
                user.email=cd['email']
                user.save()

                customer=Customer.objects.get(user=user)
                customer.address=cd['address']
                customer.save()
                messages.success(request, 'اطلاعات با موفقیت ثبت شد','success')
                url = reverse('payments:zarinpal_payment', kwargs={'order_id': order.id})
                print(f"DEBUG: The URL is {url}")
                return redirect(url)


            except ObjectDoesNotExist:
                print(">>> Order not found exception")
                messages.error(request, 'فاکتوری با این مشخصات یافت نشد','danger')
                return redirect('orders:checkout_order', order_id)
        print(">>> Form NOT valid:", form.errors)
        return redirect('orders:checkout_order', order_id)
# ______________________________________________________________________________________
# یه متد باید داشته باشم که بتونه برای من اضافه کنه کوپن رو و فقط متد پست رو میخوام چون فقط برای دکمه سابمیت کار میکنه (کاربر کد تخفیف رو اعمال میکنه و دکمه رو میزنه)
class ApplyCoupon(View):
    def post(self, request, *args, **kwargs):
        order_id=kwargs['order_id']
        coupon_form=CouponForm(request.POST)
        if coupon_form.is_valid():
            cd=coupon_form.cleaned_data
            coupon_code=cd['coupon_code']   # کد کوپن رسیده اینجا حالا باید برم چک کنم این کد کوپن وجود داره یا نه

        # حالا باید چندتا شرط بنویسم یکی اینکه این کدی که رسیده باید با کد کوپن که تو دیتا بیس هست یکی باشه و دوم این که فعال باشه و سوم اینکه در بازه تاریخ درست باشه
            coupon=Coupon.objects.filter(
                    Q(coupon_code=coupon_code) &
                    Q(is_active=True) &
                    Q(start_date__lte=datetime.now()) &
                    Q(end_date__gte=datetime.now())
                    )
        discount=0
        try:
            order=Order.objects.get(id=order_id)
            if coupon:
                discount=coupon[0].discount   # ش رو اعمال کن تو دیتا بیس میگرده و شرطهارو چک میکنه اگر درست بود تخفیف رو اعمال میکنهdiscount و coupon_code چون متد فیلتر لیست برمیگردونه بخاطر همین 0 نوشتم یعنی اولین فیلد که شرط گذاشتم که میشه
                order.discount=discount
                order.save()
                messages.success(request, 'اعمال کوپن با موفقیت انجام شد','success')
                return redirect('orders:checkout_order', order_id)
            else:
                order.discount=discount
                order.save()
                messages.error(request, 'کد وارد شده معتبر نیست','danger')
        except ObjectDoesNotExist:
            messages.error(request, 'سفارش موجود نیست')
        return redirect('orders:checkout_order', order_id)

# ______________________________________________________________________________________
# این تابع برای پاک کردن سشن موقت
def clear_session(request):
    request.session.flush()
    messages.success(request, 'سبد خرید پاک شد!')
    return redirect('orders:shop_cart')


