from django.shortcuts import render, get_object_or_404, redirect
from .models import Product,ProductGroup,FeatureValue,Brand
from django.db.models import Q, Count, Max, Min, Sum
from django.views import View
from django.http import JsonResponse
from .filters import ProductFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .compare import CompareProduct
from django.http import HttpResponse
from django.conf import settings

# _____________________________________________________________________
from django.views.generic import ListView
from .models import Product

class ProductSearchView(ListView):
    model = Product
    template_name = "products/search_results.html"
    context_object_name = "products"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Product.objects.filter(title__icontains=query)
        return Product.objects.none()

# _____________________________________________________________________
    # یه تابع نوشتم که گروه اصلی رو برای من برمیگردونه
def get_root_groop():
        return ProductGroup.objects.filter(Q(is_active=True)& Q(group_parent=None))  # برای دوتا شرط استفاده میکنمQ چون دوتا شرط میخوام بزارم هم فعال باشن (موجودی یاشه از اون کالا) هم والد نداشته باشن (خودشون ریشه باشن) از

# _____________________________________________________________________
# ارزانترین محصولات
def get_cheapest_products(request, *args, **kwargs):
    products=Product.objects.filter(is_active=True).order_by('price')[:5]   # اونایی که فعال هستن و برحسب قیمت مرتبشون کنم و از بین همشون فقط 3 تاش رو برای من بیار
    product_groups=get_root_groop()
    context={
        'products':products,
        'product_groups':product_groups
    }
    return render(request, 'products_app/partials/cheapest_products.html', context)

# _____________________________________________________________________
# # گرانترین محصولات
# def get_most_expensive_products(request, *args, **kwargs):
#     products=Product.objects.filter(is_active=True).order_by('-price')[:5]
#     product_groups=ProductGroup.objects.filter(Q(is_active=True) & Q(group_parent=None))
#     context={
#         'products':products,
#         'product_groups':product_groups
#     }
#     return render (request, 'products_app/partials/most_expensive_products.html', context)

# _____________________________________________________________________
# جدیدترین محصولات
def get_last_products(request, *args, **kwargs):
    products=Product.objects.filter(is_active=True).order_by('-published_date')[:5]   # برای اینکه بخوایم برعکسش رو بیاریم کافیه یه دش پشتش بزارم از آخر به اول واکشی میکنه
    product_groups=get_root_groop()
    context={
        'products': products,
        'product_groups': product_groups
    }
    return render(request, 'products_app/partials/last_products.html', context)

# _____________________________________________________________________
# پر فروش ترین محصولات
def get_top_selling_products(request, *args, **kwargs):
    products=Product.objects.filter(is_active=True, sales_count__gt=0).order_by('-sales_count')[:10]   # فقط 7 تای اول
    product_groups=get_root_groop()
    context={
        'products': products,
        'product_groups': product_groups
    }
    return render(request, 'products_app/partials/top_selling_products.html', context)

# _____________________________________________________________________
# گروه های محبوب
def get_popular_product_groups(request, *args, **kwargs):
    product_groups=ProductGroup.objects.filter(Q(is_active=True))\
        .annotate(count=Count('products_of_groups'))\
        .order_by('-count')[:6]  # میشماره Count برای اضافه کردن یه فیلد (همون یه ستون) که محصولات من رو به وسیله  annotate
    context={
        'product_groups': product_groups,
        'media_url': settings.MEDIA_URL
    }
    return render(request, 'products_app/partials/popular_product_groups.html',context)

# _____________________________________________________________________
# من برای خودم یه فاعده میزارم میگم هرجا پارشال دارم با تعریف تابع می نویسم هرجا میخوام یه صفحه کامل رو باز کنم با یه کلیک رو یه عکس که توضیحاتش رو کاربر ببینه کلاس تعریف میکنم
# جزئیات محصول
class ProductDetailView(View):
    def get(self, request, slug):   # اسلاگ برای این که بتونم تشخیص بدم کدوم محصول روش کلیک شده
        product=get_object_or_404(Product, slug=slug)   # این تابع میتونه برای من جستجو کنه میگم برو داخل مدل پروداکت و برای من اونی که اسلاگش برابر اسلاگ رو پیدا کن
        if product.is_active:
            return render(request, 'products_app/product_details.html', {'product':product})

# _____________________________________________________________________
# یه تابع مینویسم که یه پارشال رو فقط ران کنم که برای نشون دادن اون پایین صفحه بعد از قسمت توضیحات کامل محصول تو صفحه جزئیات عکس های مرتبط با عکس مورد نظر رو نشون بده
# محصولات مرتبط
def get_related_products(request, *args, **kwargs):
    current_product = get_object_or_404(Product, slug=kwargs["slug"])

    related_products = Product.objects.filter(
        Q(is_active=True),
        Q(product_group__in=current_product.product_group.all())
    ).exclude(
        id=current_product.id
    ).distinct()
    return render(request, 'products_app/partials/related_products.html', {'related_products':related_products})   # و این لیست رذو فرستادیم به این صفحه

# _____________________________________________________________________
# لیست کلیه گروه های محصولات
class ProductGroupsView(View):
    def get(self, request):
        product_groups=ProductGroup.objects.filter(Q(is_active=True))\
        .annotate(count=Count('products_of_groups'))\
        .order_by('-count')
        context = {
            'product_groups': product_groups,
            'media_url': settings.MEDIA_URL
        }
        return render(request, 'products_app/product_groups.html', context)

# _____________________________________________________________________
# لیست گروه محصولات برای فیلتر
# وقتی کلیک میکنم رو یه محصول وارد توضیحات اون محصول میشم سمت راست اسم  گروه های کالا رو نوشته قسمت فیلتر
def get_products_group(request):
    # annotate ایجاد کن به کمک  count بشمار و یک فیلد جدید به اسم  count به کمک
    product_groups = ProductGroup.objects.annotate(count=Count('products_of_groups'))\
                                        .filter(Q(is_active=True)& ~Q(count=0)).order_by('-count')       # فیلتر کن اول فعال باشه دوم اینکه تعداد محصولات این گروه مساوی 0 نباشه و نهایتا بر اساس تعدادی که بدست آوردم بصورت نزولی مرتب کن
    return render(request, 'products_app/partials/product_groups.html',{'product_groups':product_groups})


# _____________________________________________________________________
# لیست محصولات هر گروه محصولات
# چون میخوام یه صفحه مجزا داشته باشم و نمایش بدم از کلاس استفاده میکنم
class ProductsByGroupView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        current_group = get_object_or_404(ProductGroup, slug=slug)
        all_products = Product.objects.filter(Q(is_active=True) & Q(product_group=current_group))

        # -------------------------
        # Price range
        # -------------------------
        res_aggre = all_products.aggregate(
            min=Min('price'),
            max=Max('price')
        )

        # -------------------------
        # Apply filters (price, features, brands) from filters.py
        # -------------------------
        filter_obj = ProductFilter(request.GET, queryset=all_products)

        products = filter_obj.qs

        # -------------------------
        # Brands for this group
        # -------------------------
        brand_ids = all_products.values_list('brand_id', flat=True).distinct()
        brands = Brand.objects.filter(pk__in=brand_ids)\
                                .annotate(count=Count('product_of_brands'))\
                                .filter(~Q(count=0))\
                                .order_by('-count')

        # -------------------------
        # Features for this group
        # -------------------------
        feature_list = current_group.features_of_groups.all()
        feature_dict = {}
        for feature in feature_list:
            feature_dict[feature] = feature.feature_values.all()

        # Selected features from GET
        selected_features = request.GET.getlist('feature')

        # -------------------------
        # sort type
        # -------------------------
        sort_type=request.GET.get('sort_type')
        if not sort_type:
            sort_type='0'
        if sort_type=='1':
            products=products.order_by('price')
        elif sort_type=='2':
            products=products.order_by('-price')

        # -------------------------
        # Paginator & Display Count
        # -------------------------
        count = request.GET.get('count', '12')  # ۱. گرفتن تعداد نمایش از کاربر (پیش‌فرض ۱۲)
        try:
            count_int = int(count)
        except (ValueError, TypeError):
            count_int = 12
        page = request.GET.get('page', 1)  # ۲. گرفتن شماره صفحه از URL
        paginator = Paginator(products, count_int)  # ۳. ساخت Paginator با تعداد متغیر

        try:
            products_page = paginator.page(page)
        except PageNotAnInteger:
            products_page = paginator.page(1)
        except EmptyPage:
            products_page = paginator.page(paginator.num_pages)

        user = request.user
        for product in products_page:
            product.is_favorite = product.get_user_favorite(user)

        # -------------------------
        # Product groups for sidebar
        # -------------------------
        product_groups = ProductGroup.objects.annotate(
            count=Count('products_of_groups')
        ).filter(
            Q(is_active=True) & ~Q(count=0)
        ).order_by('-count')

        return render(request, 'products_app/products.html', {
            'products': products_page,
            'page_obj': products_page,
            'paginator': paginator,
            'filter_obj': filter_obj,
            'current_group': current_group,
            'group_slug': slug,
            'price_min': res_aggre['min'] or 0,
            'price_max': res_aggre['max'] or 0,
            'brands': brands,
            'feature_dict': feature_dict,
            'selected_features': selected_features,
            'product_groups': product_groups,     # صفحه فعلی برای قالب
            'title': current_group.group_title,
            'group_image': current_group.image_name.url if current_group.image_name else '',
            'group_description': current_group.description,
            'selected_count': str(count_int),
            'sort_type': sort_type,

        })

# _____________________________________________________________________
# تابع برای ایجکس تو پوشه ادمین اسکریپت.جی اس/جی اس برای دراپ داون پنل ادمین
def get_filter_value_for_feature(request):
    if request.method=='GET':
        feature_id=request.GET['feature_id']
        feature_values=FeatureValue.objects.filter(feature_id=feature_id)
        res={fv.value_title : fv.id for fv in feature_values}
        return JsonResponse(res, safe=False)

# _____________________________________________________________________
# لیست برندها برای فیلتر
def get_brands(request, *args, **kwargs):
    product_group=get_object_or_404(ProductGroup, slug=kwargs['slug'])   # رو صدا میزنم اسلاگ گروه رو براش فرستادم از رو اسلاگ گروه رو پیدا کردم render_partials اونجایی که دارم
    brand_list_id=product_group.products_of_groups.filter(is_active=True).values('brand_id')  # از روی گروهی که پیدا کردم محصولات گروه رو پیدا کردم و فقط آیدیه برندهای محصولات این گروه رو کشیدم بیرون
    # هست brand_list_id بعد رفتم تو جدول برندها فیلتر کردم اون هایی که کد اصلیشون درون
    brands = Brand.objects.filter(pk__in=brand_list_id)\
                            .annotate(count=Count('product_of_brands'))\
                            .filter(~Q(count=0))\
                            .order_by('-count')
    return render(request, 'products_app/partials/brands.html', {'brands':brands})

# _____________________________________________________________________
# لیست فیلتر ها بر حسب مقادیر ویژگی های درون کالا انتخاب شده توسط کاربر
def get_features_for_filter(request, *args, **kwargs):
    product_group=get_object_or_404(ProductGroup, slug=kwargs['slug'])   # اول چک میکنیم ببینیم گروهمون چیه
    feature_list=product_group.features_of_groups.all()   # وقتی گروه رو پیدا کردم ببینم گروه ها مرتبط با ویژگیشه درواقع از روی گروه میتونم ویژگی هاش رو در بیارم
    feature_dict=dict()   # برای اینکه مقادیر ویژگی برای ویژگی هر کالا رو بهش دسترسی پیدا کنم باید باید یک دیشکنری بسازم
    for feature in feature_list:
        feature_dict[feature]=feature.feature_values.all()    # feature_dict = {ram:[4GB, 8GB, 16GB]} موقع دراپ داون کردن اون پایین تو پنل ادمین مقادیر مربوط به خودش رو هر کالا نشون بده و هم اینکه تو صفحه وب سمت راست قسمت فیلتر ها وقتی یه گروهی از کالا ها رو انتخب میکنیم اونجا هم مقادیر ویژگی مربوط به هر گروه رو وقتی دراپ داون میکنه کاربر نشون میده بهش الان فیچر میشه کلید فیچر ولیو هم میشه ولیو
    return render(request, 'products_app/partials/features_filter.html', {'feature_dict':feature_dict})

# _____________________________________________________________________
# بساز CompareProduct صفحه اصلی مقایسه: نمایش کالاهای اضافه شده به لیست مقایسه، هربار اینو صدا زدم میگم برو یه نمونه از اون کلاس
class ShowCompareListView(View):
    def get(self, request, *args, **kwargs):
        compare_list=CompareProduct(request)
        return render(request, 'products_app/compare_list.html', {'compare_list':compare_list})

# _____________________________________________________________________
# نمایش جدول کالاهای لیست مقایسه: این تابع مهمترین بخش از تابع مقایسه هست که بصورت جدول نشون میدم
def compare_table(request):
    compareList=CompareProduct(request)  # زمانی که یک شی از یه کلاس درست میکنیم صفنهخای اونو الان داره
    products=[]

    # توی این فرایند کالاها بدست میان
    for productId in compareList.compare_product:
        product=Product.objects.get(id=productId)
        products.append(product)

    features=[]
    for product in products:
        for item in product.product_features.all():
            if item.feature not in features:
                features.append(item.feature)

    context = {
        'products':products,
        'features': features
    }
    return render(request, 'products_app/partials/compare_table.html', context)

# _____________________________________________________________________
# محاسبه تعدادکالاهای موجود در لیست مقایسه
def status_of_compare_list(request):
    compareList=CompareProduct(request)
    return HttpResponse(compareList.count)

# _____________________________________________________________________
# اضافه کردن کالا به لیست مقایسه
# به سشن اضافه میکنه compare.py این ویو برای من یه پروداکت اید میگیره میبره تو فایل
def add_to_compare_list(reqeust):
    productId=reqeust.GET.get('productId')
    # productGroupId=request.GET.get('productGroupId')
    compareList=CompareProduct(reqeust)
    compareList.add_to_compare_product(productId)
    return HttpResponse('کالا به لیست مقایسه اضافه شد')

# _____________________________________________________________________
# حذف کالا از لیست مقایسه
def delete_from_compare_list(request):
    productId=request.GET.get('productId')
    compareList=CompareProduct(request)
    compareList.delete_from_compare_product(productId)
    return redirect("products:compare_table")

