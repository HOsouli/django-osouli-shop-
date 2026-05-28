from django.db import models
from apps.orders.models import Order
from apps.accounts.models import Customer
from django.utils import timezone

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment_order', verbose_name='سفارش')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payment_customer', verbose_name='مشتری')
    register_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ پرداخت')
    update_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش پرداخت')
    amount = models.DecimalField(max_digits=15, decimal_places=0, verbose_name='مبلغ پرداخت')
    description = models.TextField(verbose_name='توضیخات پرداخت')
    is_finaly = models.BooleanField(default=False, verbose_name='وضعیت پرداخت')  # ش میکنیمTrue بعد از اینکه از درگاه برمیگرده اگه پرداخت کرده بود  False لحظه اول

# نکته خیلی مهم حتما حتما همیشه برای درگاه های پرداخت این دوتا فیلد رو باید در نظر بگیریم
    status_code = models.IntegerField(verbose_name='کد وضعیت درگاه پرداخت', null=True, blank=True)  # استفاده کنیم و اینکه چون اول کار ما اینو نداریم اول کار باید نال و بلنکش رو تورو کنیم IntegerField این کد وضعیت یه کدیه که همه درگاه های پرداخت داره و ما بهتره بنویسیم اینو و ذخیره کنیم و چون یه عدد باید از
    ref_id = models.CharField(max_length=50, verbose_name='کد پیگیری پرداخت', null=True, blank=True)  # بگیریمش CharField یکی دیگه هم رفرنس آیدیه که درواقع کد پیگیریه زمانی که مشتری مبلغ رو پرداخت میکنه یه کدی میده که برای تایید بودن هزینه پرداخت که باید از جنس

    def __str__(self):
        return f"{self.order} {self.customer} {self.ref_id}"

    class Meta:
        managed = True
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت‌ها'
