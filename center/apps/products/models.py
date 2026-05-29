from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from utils import FileUpload
from ckeditor_uploader.fields import RichTextUploadingField
# from ckeditor.fields import RichTextField
from django.urls import reverse
from datetime import datetime
from django.db.models import Sum,Avg

# ______________________________________________________________________________
from utils import FileUpload
class Brand(models.Model):
    brand_title = models.CharField(max_length=100, verbose_name='نام برند')
    file_upload = FileUpload('images','brand')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصویر برند کالا')
    slug = models.SlugField(max_length=200, blank=True, unique=True)

    def __str__(self):
        return self.brand_title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.brand_title, allow_unicode=True)
            slug = base_slug
            n = 1
            while Brand.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)


    class Meta:
        managed = True
        verbose_name = 'برند'
        verbose_name_plural = 'برندها'
# ______________________________________________________________________________
class ProductGroup(models.Model):
    group_title = models.CharField(max_length=100, verbose_name='عنوان گروه کالا')
    file_upload = FileUpload('images','product_group')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصویر گروه کالا')
    description = RichTextUploadingField(blank=True, null=True, config_name='admin_full', verbose_name='توضیحات')
    is_active = models.BooleanField(default=True, blank=True, verbose_name='وضعیت فعال / غیرفعال')
    group_parent = models.ForeignKey(
        'ProductGroup',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='والد گروه کالا',
        related_name='groups'
        )
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')
    published_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ انتشار')
    update_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین به روزرسانی')
    slug = models.SlugField(max_length=200, blank=True, unique=True)

    def __str__(self):
        return self.group_title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.group_title,allow_unicode=True)
            slug = base_slug
            n = 1
            while ProductGroup.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)


    class Meta:
        managed = True
        verbose_name = 'گروه کالا'
        verbose_name_plural = 'گروه های کالا'
# ______________________________________________________________________________
class Feature(models.Model):
    feature_name = models.CharField(max_length=100, verbose_name='نام ویژگی')
    product_group = models.ManyToManyField(ProductGroup, verbose_name='گروه کالا', related_name='features_of_groups')

    def __str__(self):
        return self.feature_name

    class Meta:
        managed = True
        verbose_name = 'ویژگی'
        verbose_name_plural = 'ویژگی‌ها'
# ______________________________________________________________________________
class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name='نام کالا')
    summery_description = models.TextField(default="", blank=True, null=True, verbose_name='شرح کالا')
    description = RichTextUploadingField(blank=True, null=True, config_name='admin_full', verbose_name='توضیحات')
    file_upload = FileUpload('images', 'products')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصویر کالا')
    price = models.DecimalField(max_digits=15, decimal_places=0, default=0, verbose_name='قیمت کالا')
    sales_count = models.IntegerField(default=0, verbose_name=' (پرفروش‌ها) تعداد فروش')
    product_group = models.ManyToManyField(ProductGroup, verbose_name='گروه کالا', related_name='products_of_groups')
    features = models.ManyToManyField(Feature, through='ProductFeature')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='برند کالا', null=True, related_name='product_of_brands')
    is_active = models.BooleanField(default=True, blank=True, verbose_name='وضعیت فعال / غیرفعال')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')
    published_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ انتشار')
    update_date = models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین به روزرسانی')
    slug = models.SlugField(max_length=200, blank=True, unique=True)


    def __str__(self):
        return self.product_name


    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.product_name, allow_unicode=True)
            slug = base_slug
            n = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)


    # استفاده میکنیم که این تابع قرار آدرس یه صفحه رو برای من برگردونه مثلا زدم رو یه کالا بره تو صفحه دیگه برای توضیحاتش get_absolute_url هرزمان که ما مدلی داشتیم که مدام نیاز شد به اون دسترسی داشته باشیم از متد
    def get_absolute_url(self):
        return reverse('products:product_details', kwargs={'slug': self.slug})  # نوشتم urls.py برای آدرس دهیه که باید ایمپورت شه پارامتر اولش میشه آدرس یه صفحه که بهش میدیم پارامتر دوم اسلاگش یعنی اون نمونه ای که باعث فراخوانی میشه اسلاگش رو بردار بریز تو اسلاگ و به اون آدرس ارسالش کن، آدرسش رو من تو reverse


    # این تابع برای اینه که هر کالا میزان تخفیف خودش رو بر اساس قیمت خودش محاسبه میکنه وبهای تمام شده بعد از تخفیف رو نشون میده
    def get_price_by_discount(self):
        lst=[]
        today = datetime.now().date()  # ← یکبار تعریف کن
        for dbd in self.discount_basket_details2.all():   # اضافه شده بود به مدل پروداکتم رو اینجا میارم بهای تمام شده هر کالا با تخفیفش محاسبه کنه related_name توسط  discount_basket_details2 این
            if (dbd.discount_basket.is_active and
                dbd.discount_basket.start_date <= today and      # ← today
                today <= dbd.discount_basket.end_date):          # ← today
                lst.append(dbd.discount_basket.discount)
        discount = max(lst) if lst else 0
        final_price = self.price - (self.price * discount / 100)
        return int(final_price)


# صداش بزنم بهم میگه چندتا از اون کالا وجود داره (تعداد موجودی کالا در انبار) Product یه تابع نوشتم که هرجایی از پروژم توسط
    def get_number_in_warehouse(self):
        sum1=self.warehouse_product.filter(warehouse_type_id=1).aggregate(sum('quantity'))   # اونایی که 1 هستن یعنی خرید، جمع شون چند میشه یعنی چندتا خریدن موجودیش رو ببین چندتاس warehouse_type_id ش رو نگاه کن ورودی و خروجی هاش رو بدست بیار و فیلد warehouse_product که میشه همون کالای جاری میگم self
        sum2=self.warehouse_product.filter(warehouse_type_id=2).aggregate(sum('quantity'))   # و همینطور مجموع فروش اون کالا
        input=0
        if sum1['quantity__sum']!=None:   # امکان داره کالایی نه وارد شده نه خارج شده و نان برگردونه یه متغیر به کمک مثلا اینپوت تعریف کردم گفتم اگر نان نبود بگیرش بریز تو اینپوت، اینپوت تعداد ورودی از این کالاس
            input=sum1['quantity__sum']
        output=0
        if sum2['quantity__sum']!=None:   # آوتپوت تعداد خروجی از این کالاس
            output=sum2['quantity__sum']

        return input-output   # میگم هرجندتا خریدم و هرچندتا فروختم تعداد کالاهای موجودیم میشه


# میزان امتیازی که کاربر جاری به کالا داده
    def get_user_score(self, user):
        if not user or not user.is_authenticated:
            return 0

        user_score = self.scoring_product.filter(scoring_user=user).first()
        if user_score:
            return user_score.score
        return 0



# میانگین امتیازی که این کالا کسب کرده
    def get_avrage_score(self):
        avgScore=self.scoring_product.all().aggregate(Avg('score'))['score__avg']
        # avg_score = self.scoring_product.all().aggregate(avg=Avg('score'))['avg']  # استفاده نکنیم این روش بهتره حتی چون روش استاد قدیمیتره ['score__avg'] به حای خط بالایی استفاده کرد که دیگه از دوتا آندرلاین مثلا اینجوری aggregate یا به این روش هم میشه از
        if not avgScore:
            avgScore=0
        return avgScore


# آیا این کالا مورد علاقه کاربر جاری بوده یا خیر
    def get_user_favorite(self, user):
        if not user or not user.is_authenticated:
            return False

        return self.favorite_product.filter(favorite_user=user).exists()



# تابع برای برگرداندن گروه اصلی کالا
    def getMainProductGroup(self):
        return self.product_group.all()[0].id

    class Meta:
        managed = True
        verbose_name = 'کالا'
        verbose_name_plural = 'کالاها'
# ______________________________________________________________________________
# کلاسی تعریف کردیم برای فیلترینگ که نشون بده هر ویژگی یه مقدار داره
# به طور مثال یه رم گیگ های مختلف داره یا مثلا یه لباس سایزهای مختلف داره در کل یه ویژگی میتونه چندین مقدار داشته باشه
class FeatureValue(models.Model):
    value_title=models.CharField(max_length=100, verbose_name='عنوان مقدار')
    feature=models.ForeignKey(Feature, on_delete=models.CASCADE, blank=True, null=True, verbose_name='ویژگی', related_name='feature_values')

    def __str__(self):
        return f"{self.id}  {self.value_title}"

    class Meta:
        managed = True
        verbose_name = 'مقدار ویژگی'
        verbose_name_plural = 'مقادیر ویژگی‌ها'
# ______________________________________________________________________________
# نوشتم و با تعریف کردن این مدل عملا ما میتونیم هر چندتا فیلد بخوایم بهش اضافه کنیم Product میتونم به تمام ویژگی ها و کالا ها وصل بشم که تو خط 82 تو کلاس  through= با تعریف کردن این کلاس همون رابطه چند به چند بین کالا و ویژگی اتفاق افتاد اما مشکل اینه که کالاهای ما نمیتونن این کلاس رو پیدا کنن اما به کمک
class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='کالا', related_name='product_features')
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE, verbose_name='ویژگی')
    value = models.CharField(max_length=100, verbose_name='مقدار ویژگی کالا')
    filter_value=models.ForeignKey(FeatureValue, on_delete=models.CASCADE, blank=True, null=True, verbose_name='فیلتر بر اساس مقدار ویژگی')

    def __str__(self):
        return f"{self.product} - {self.feature}: {self.value}"  # از کالا با ویژگیه خاص چند مقدار وجود داره

    class Meta:
        managed = True
        verbose_name = 'ویژگی محصول'
        verbose_name_plural = 'ویژگی های محصولات'
# ______________________________________________________________________________
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='کالا', related_name="gallery_images")   # اضافه کنم تا بتونم با کلاس محصول ارتباط بگیرم و عکس هارو با حلقه تو تمپلیت جزئیات محصول عکس ها رو اضافه کنم Product برای اینه که یه فیلد به کلاس  related_name این
    file_upload = FileUpload('images','product_gallery')
    image_name = models.ImageField(upload_to=file_upload.upload_to, verbose_name='تصویر کالا')

    class Meta:
        managed = True
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'

# ______________________________________________________________________________

