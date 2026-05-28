from django.db import models
from apps.products.models import Product
from apps.accounts.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator

# _________________________________________________________________________________________________
class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments_product', verbose_name='کالا')
    commenting_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cumments_user1', verbose_name='کاربر نظر دهنده')
    approving_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cumments_user2', verbose_name='کاربر تایید کننده نظر', null=True, blank=True)
    comment_text = models.TextField(verbose_name='متن نظر')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')
    is_active = models.BooleanField(default=False, verbose_name='وضعیت')
    comment_parent = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, blank=True, related_name='comments_child')  # رو به بدیم بهش و نکته خیلی مهم اینه که هر زمان که یک مدل به خودش میخواد فارن کی بزنه حتما حتما باید بصورت رشته بنویسیم که قبلا هم گفته بودم Comment نظری که اول ثبت میشه والد نظر نداره پس فیلد والد نظرشون نال هست ولی ممکن نفر دومی جواب نظر والد رو بده اینجا باید مدل

    def __str__(self):
        return f'{self.product} - {self.commenting_user}'

    class Meta:
        managed = True
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

# _________________________________________________________________________________________________
class Scoring(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='scoring_product', verbose_name='کالا')  # امتیاز دهی روی یک کالا
    scoring_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='scoring_user1', verbose_name='امتیاز دهنده')  # توسط کاربر
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name='امتیاز')  # مقدار امتیاز

    def __str__(self):
        return f"{self.product} - {self.scoring_user}"

    class Meta:
        managed = True
        verbose_name = 'امتیاز'
        verbose_name_plural = 'امتیازات'

# _________________________________________________________________________________________________
class Favorite(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorite_product', verbose_name='کالا')  # چه کالایی
    favorite_user=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorite_user1', verbose_name='کاربر علاقه مند')  # مورد علاقه چه کاربری بوده
    register_date=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')  # تو چه تاریخی ثبت شده

    def __str__(self):
        return f"{self.product} - {self.favorite_user}"

    class Meta:
        managed = True
        verbose_name = 'علاقه'
        verbose_name_plural = 'علایق'
