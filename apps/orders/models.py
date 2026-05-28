from django.db import models
from apps.accounts.models import Customer
from apps.products.models import Product
from django.utils import timezone
import uuid
import utils
# ______________________________________________________________________________
class PaymentType(models.Model):
    payment_title = models.CharField(max_length=50, verbose_name='نوع پرداخت')

    def __str__(self):
        return self.payment_title

    class Meta:
        managed = True
        verbose_name = 'نوع پرداخت'
        verbose_name_plural = 'انواع پرداخت'
# ______________________________________________________________________________
class OrderState(models.Model):
    order_state_title = models.CharField(max_length=50, verbose_name='وضعیت سفارش')

    def __str__(self):
        return self.order_state_title

    class Meta:
        managed = True
        verbose_name = 'وضعیت سفارش'
        verbose_name_plural = 'انواع وضعیتهای سفارش'
# ______________________________________________________________________________
# سفارش مال کیه
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', verbose_name='مشتری')
    register_date = models.DateField(default=timezone.now, verbose_name='تاریخ درج سفارش')
    update_date = models.DateField(auto_now=True, verbose_name='تاریخ ویرایش سفارش')
    is_finally = models.BooleanField(default=False, verbose_name='نهایی شده')
    order_code = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='کد تولیدی برای سفارش')   # کد سفارش که بصورت یونیکه (اختیاری هست این فیلد چون خودش داره) یه کد طولانی منحصر به فرد تولید میکنه این فیلد و اجازه هم ندم که قابل تغییر باشه
    discount = models.IntegerField(blank=True, null=True, default=0, verbose_name='تخفیف روی فاکتور')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    payment_type = models.ForeignKey(
                            PaymentType, default=None, on_delete=models.CASCADE,
                            null=True, blank=True, verbose_name='نوع پرداخت',
                            related_name='payment_types')   # کنیم True ش روblank و null هروقت بعدن بخوایم به مدل هامون فیلد اضافه کنیم حتما باید
    order_state = models.ForeignKey(
                            OrderState, on_delete=models.CASCADE,
                            null=True, blank=True, verbose_name='وضعیت سفارش',
                            related_name='orders_states'
                                    )   # که ادمین بررسی میکنه وضعیت سفارش چگونسOrderState این فیلد درواقع یه کلید خارجی از جدول

    def get_order_total_price(self):
        total = 0
        for item in self.order_details1.all():
            total += item.price * item.quantity
        order_final_price, delivery, tax = utils.price_by_delivery_tax(total, self.discount)
        return int(order_final_price)


    def __str__(self):
        return f"{self.customer}\t{self.id}\t{self.is_finally}"

    class Meta:
        managed = True
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'

# ______________________________________________________________________________
# سفارش شامل چه کالاهاییه
class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details1', verbose_name='سفارش')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_details2',)
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')
    price = models.DecimalField(max_digits=15, decimal_places=0, default=0, verbose_name='قیمت کالا در فاکتور')

    def __str__(self):
        return f"{self.order}\t{self.product}\t{self.quantity}\t{self.price}"



