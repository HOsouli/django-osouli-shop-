from django.db import models
from utils import FileUpload
from django.utils import timezone
from django.utils.html import mark_safe

class Slider(models.Model):
    slider_title1 = models.CharField(max_length=500, blank=True, null=True, verbose_name='متن اسلایدر اول')
    slider_title2 = models.CharField(max_length=500, blank=True, null=True, verbose_name='متن اسلایدر دوم')
    slider_title3 = models.CharField(max_length=500, blank=True, null=True, verbose_name='متن اسلایدر سوم')
    file_upload = FileUpload('images','slides')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصویر اسلاید')
    slider_link = models.URLField(max_length=200, null=True, blank=True, verbose_name='لینک')  # این فیلد برای این نوشتم که کاربر کلیک کرد رو عکس اسلایدر مثلا هرکدوم از اسلایدر ها بره یه صفحه ای با یو آرال دیگه ای رو باز کنه بلنک و نال رو تورو گذاشتم که اگه نخواست لینک نده به اسلایدر ها
    is_active = models.BooleanField(default=True, blank=True, verbose_name='وضعیت فعال/غیرفعال')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    published_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ انتشار')
    update_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین به روز رسانی')

    def __str__(self):
        return self.slider_title1 or self.slider_title2 or f"اسلایدر #{self.id}"

    class Meta:
        managed = True
        verbose_name = 'اسلاید'
        verbose_name_plural = 'اسلایدها'


# یک تگ اچ تی ام ال رو میگیره و اونو اجرا میکنه که ایمپورت باید بشه این رو برای نشون دادن عکس اسلاید تو خود پنل ادمین نوشتم که ادمین بتونه تو پنل ادمین عکس هارو تو ستون اول ببینه و بتونه مدیریت کنه اسلایدهارو عوض کنه mark_safe
    def image_slide(self):
        return mark_safe(f'<img src="/media/{self.image_name}" style= "width: 80px; height: 60px;"/>')

    image_slide.short_description = 'تصویر اسلاید'


# که میزنه قابل کلیک باشه که ببره به یه صفحه مشخص دیگه link تو مدلم نوشتم برای اون یه لینک بدم که هم تو اسلایدر صفحه وب قابل کلیک باشه هم تو پنل ادمین رو کلمه slider_link برای اسلایدرم که فیلد link حالا میخوام یه
    def link(self):
        return mark_safe(f'<a href="{self.slider_link}" target="_blank">link</a>')

    link.short_description = "پیوندها"


