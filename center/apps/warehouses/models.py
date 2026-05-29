from django.db import models
from apps.products.models import Product
from apps.accounts.models import CustomUser

# ___________________________________________________________________________________
# منظور از این کلاس نوع انبار همون خرید کردن فروش کردن مرجوعی امانت دادن امانت گرفتنن معیوبی و غیره
class WarehouseType(models.Model):
    warehouse_type_title = models.CharField(max_length=50, verbose_name='نوع انبار')

    def __str__(self):
        return self.warehouse_type_title

    class Meta:
        managed = True
        verbose_name = 'نوع انبار'
        verbose_name_plural = 'انواع روش انبار'

# ___________________________________________________________________________________
# داریم WarehouseType تو کلاس انبار من سه تا کلید خارجی دارم آیا خریده آیا فروشه آیا مرجوعیه آیا معیوبه پس یه مدل کلید خارجی به
# انبار توسط کی اتفاق میوفته چه یوزری داره کالا رو به انبار اضافه یا خارج میکنه مثلا صاحب قروشگاه صدتا پفک خریده و ادمین به انبار اضافه کرده اما اگه مشتری خرید کنه پس کشتری داره از انبار خارج میکنه پس یا مدیر داره به انبار اضافه میکنه یا مشتری داره خارج میکنه از انبار
# و اینکه چه محصولی رو داریم از انبار خارج میکنیم یا وارد میکنیم
class Warehouse(models.Model):
    warehouse_type = models.ForeignKey(WarehouseType, on_delete=models.CASCADE, related_name='Warehouse', verbose_name='انبار')
    user_registered = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='warehouseuser_registered', verbose_name='کاربر انباردار')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='warehouse_product', verbose_name='کالا')
    quantity = models.IntegerField(verbose_name='تعداد')
    price = models.DecimalField(max_digits=15, decimal_places=0, default=0, verbose_name='قیمت', null=True, blank=True)
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    def __str__(self):
        return f'{self.warehouse_type} - {self.product}'

    class Meta:
        managed = True
        verbose_name = 'انبار'
        verbose_name_plural = 'انبارها'

