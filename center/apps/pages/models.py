from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField

class StaticPage(models.Model):
    PAGE_TYPES = [
        ('about', 'درباره ما'),
        ('contact', 'تماس با ما'),
        ('rules', 'قوانین و مقررات')
    ]

    title = models.CharField(max_length=100, verbose_name='عنوان')
    content = RichTextUploadingField(config_name='admin_full', verbose_name='محتوا')
    page_type = models.CharField(max_length=20, choices=PAGE_TYPES, verbose_name='نوع صفحه')
    is_active = models.BooleanField(default=True, verbose_name='وضعیت فعال/غیرفعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        managed = True
        verbose_name = 'صفحه ثابت'
        verbose_name_plural = 'صفحات ثابت'

