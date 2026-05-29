from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.products.models import Product

# _____________________________________________________________________________________
# کوپن تخفیف
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10, unique=True, verbose_name='کد کوپن')   # و حتما باید یونیک کنم برای اینکه یبار به اون مشتری تخفیف دادیم دیگه بهش دوباره تخفیف نده
    start_date = models.DateField(verbose_name='تاریخ شروع')   # تاریخ شروع کوپن
    end_date = models.DateField(verbose_name='تاریخ پایان')    # تاریخ پایان کوپن
    discount = models.IntegerField(verbose_name='درصد تخفیف', validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(verbose_name='وضعیت', default=False)

    class Meta:
        managed = True
        verbose_name = 'کوپن تخفیف'
        verbose_name_plural = 'کوپن‌ها'

    def __str__(self):
        return self.coupon_code

# ____________________________________________________________________________________
# سبد تخفیف (شامل مناسبتها)
# فرقش با کلاس بالایی اینه که یه سبد چنتا کالا توش داره که یه مدل مجزا جزئیاتش رو میارم
class DiscountBasket(models.Model):
    discount_title = models.CharField(max_length=100, verbose_name='عنوان سبد خرید')
    start_date = models.DateField(verbose_name='تاریخ شروع')   # تاریخ شروع کوپن
    end_date = models.DateField(verbose_name='تاریخ پایان')    # تاریخ پایان کوپن
    discount = models.IntegerField(verbose_name='درصد تخفیف', validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(verbose_name='وضعیت', default=False)

    class Meta:
        managed = True
        verbose_name = 'سبد تخفیف'
        verbose_name_plural = 'سبدهای تخفیف'

    def __str__(self):
        return self.discount_title

# ____________________________________________________________________________________
class DiscountBasketDetails(models.Model):
    discount_basket = models.ForeignKey(DiscountBasket, on_delete=models.CASCADE, verbose_name='سبد تخفیف', related_name='discount_basket_details1')   # میخوره DiscountBasket جزئبات مربوط به کدوم سبد این ریلیتد نیم ارتباطیه که با کلاس
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='کالا', related_name='discount_basket_details2')   # نوشته میشه عملا به مدل پروداکتم اضافه میشه related_name توسط Product داخل چه سبدی چه کالاهایی وجود داره و این ریلیتد نیم هم ارتباط این فیلد که به مدل

    class Meta:
        managed = True
        verbose_name = 'جزئیات سبد تخفیف'

