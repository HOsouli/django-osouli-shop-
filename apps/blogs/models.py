from django.db import models
from django.utils.text import slugify
from utils import FileUpload
from django.conf import settings
from apps.products.models import Product
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.urls import reverse

class BlogGroup(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان دسته‌بندی')
    description = RichTextUploadingField(blank=True, null=True, config_name='admin_full', verbose_name='توضیحات')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='اسلاگ')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'دسته‌بندی بلاگ'
        verbose_name_plural = 'دسته بندی‌های بلاگ'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
            slug = base_slug
            counter = 1
            while BlogGroup.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

# ______________________________________________________________________________________
# مینویسم Post.published.all() کوئری بنویسیم خیلی تمیز تر با تعریف این کلاس به این شکل Post.objects.filter(is_active=True, is_published=True) این کلاس رو میشه تو هر مدلی تعریف کرد بخاطر اینکه کدهامون تو ویو کوتاه تر و تمیز تر باشه مثلا بجای اینکه توی ویو اینطوری
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, is_published=True)

class Post(models.Model):
    """
    مدل پست بلاگ.
    - blog_group: دسته‌بندی‌های مرتبط (رابطه چندبه‌چند)
    - related_products: محصولات مرتبط با مقاله (برای لینک به فروشگاه)
    """
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(max_length=250, unique=True, blank=True, verbose_name='اسلاگ')
    content = RichTextUploadingField(config_name='admin_full', verbose_name='محتوا')
    views = models.PositiveIntegerField(default=0, verbose_name='تعداد بازدید')
    file_upload = FileUpload('images', 'blogs')
    image_name = models.ImageField(upload_to=file_upload.upload_to, blank=True, null=True, verbose_name='تصویر مقاله')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='blog_posts', verbose_name='نویسنده')

    # بتونم به پستهاش دسترسی داشته باشم BlogGroup میدیم چون میخوام از سمت related_name وصل شود اینجا BlogGroup نکته خیلی مهم که چرا از چند به چند استفاده کردم یک پست می‌تواند در چند دسته باشد و یک دسته می‌تواند چند پست داشته باشد فرض کن این دسته‌ها را داریم: راهنمای خرید، مقایسه و آموزش و این مقاله مقایسه بهترین گوشی‌های اقتصادی برای خرید داره هم راهنمای خرید هم مقایسه است پس باید بتواند به
    blog_group = models.ManyToManyField(BlogGroup, related_name='posts', blank=True, verbose_name='دسته بندی‌ها')

    # به مقاله‌ها دسترسی داشته باشیم Product این اجازه می‌دهد از سمت related_name=‘related_blog_posts’ نکته: خیلی از مقاله‌های بلاگ درباره محصولات هستند. مثلا: راهنمای خرید بهترین لپ‌تاپ برای برنامه‌نویسی و در داخل مقاله ممکن است چند محصول معرفی شود پس یک پست می‌تواند چند محصول مرتبط داشته باشد و از طرف دیگر یک محصول هم می‌تواند در چند مقاله معرفی شود و
    related_products = models.ManyToManyField(Product, related_name='related_blog_posts', blank=True, verbose_name='محصولات مرتبط')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')
    is_published = models.BooleanField(default=False, verbose_name='منتشر شده')
    register_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ثبت')
    published_date = models.DateTimeField(blank=True, null=True, verbose_name='تاریخ انتشار')
    update_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    # به کلاس Post Manager اضافه کردن
    objects = models.Manager()     # manager پیش‌فرض
    published = PublishedManager() # فقط پست‌های منتشر شده

    class Meta:
        verbose_name = 'پست بلاگ'
        verbose_name_plural = 'پست‌های بلاگ'
        ordering = ['-published_date', '-register_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        # ساخت اسلاگ یکتا با شمارنده
        if not self.slug:
            base_slug = slugify(self.title, allow_unicode=True)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        # تنظیم تاریخ انتشار در لحظه‌ای که منتشر می‌شود
        if self.is_published and not self.published_date:
            self.published_date = timezone.now()
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse( 'blogs:post_detail', kwargs={'slug': self.slug})


