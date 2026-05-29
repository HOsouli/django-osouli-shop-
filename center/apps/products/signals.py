from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from .models import Product
from apps.warehouses.models import Warehouse
from django.conf import settings
from django.db.models import Sum
import os

# سیگنال هایی که برای کار کردن با دیتا بیس ازشون استفاده میکنیم
# رو داشته باشه kwargs و sender مدلیه که این مدل پایین که کارش دیلیت کردنه سیگنال رو ارسال میکنه مثل مدل کالا که هربار که یه اتفاقی مثل دیلیت شدن براش میوفته باید سریع یه سیگنال به این تابع بفرسته و تابعی که دریافت کننده سیگناله باید دوتا پارامتر sender یعنی دریافت کننده سیگنال کیه که میشه نام اون تابعی که قرار سیگنال رو دریافت کنه و دومی receiver و دوتا مقدار بهش میدم یکی connect ش رو ایمپورت میکنیم از پست دیلیت میخوام کانکت شه با متد post_delete مثلا
# برای زمانیه که وقتی ادمین یه کالا رو حذف میکنه رکورد حذف میشه تو دیتا بیس اما تو پوشه عکس میمونه و این خوب نیست

# # این تابع فقط برای اینکه که وقتی از پنل ادمین یه کالا رو حذف کردیم تو محیط ترمینال وی اس کد پرینت میشه کالا حذف شد با ستاره های بالا و پایین
# def delete_product_image(sender, **kwargs):
#     print(100*"*")
#     print("Product deleted...")
#     print(100*"*")

# post_delete.connect(receiver=delete_product_image, sender=Product)

# ________________________________________________________________________________________________
# استفاده کنیم کافیه دکوراتور رسیور استفاده کنم و دوتا ورودی بهش بدم یکی اسم سیگنال دومی مشخص کنم کی این سیگنال رو تولید کنه بعد از حذف شدن پروداکت تو اجرا شوconnect ولی روش بهتر استفاده از دکوراتوره اینجا دیگه نیازی نیست از
# حتما اضافه بشه ready تابع apps.py بعدش اسنیپت اتومات خودش نشونش میده و اینتر بزنی، تعریف کردن این تابع به این دلیله که خود سیستم این کدها رو نمیبینه و بصورت پیشفرض این کد اجرا نمیشه به همین دلیل باید تو def ready حتما باید اضافه کنی که من اضافه کردم کافیه بنویسی apps.py رو به ready فقط نکته اگه از این روش که توضیه میشه و بهترم هست اصتفاده کردی تابع

@receiver(post_delete, sender=Product)
def delete_product_image(sender, **kwargs):
    print(100*"*")
    print("Product deleted...")
    print(100*"*")
    path=settings.MEDIA_ROOT+str(kwargs['instance'].image_name)  # خواستم تو این مسیر ببین آیا این فایل وجود داره اگه داره حذفش کن os از ماژول path که اشاره داره به کل اون رکوردی که سیگنال رو برامون داره میفرسته سطری که برامون حذف میشه این 'instance' که به عنوان ورودی تابعمون بود یک دیکشنریه و یکی از فیلدای این دیکشنری kwargs
    if os.path.isfile(path):
        os.remove(path)
        print(f"deleted: {path}")

# _______________________________________________________________________________________________
# SIGNAL: هر OrderItem ذخیره بشه:
# 1. کل تعداد‌های اون محصول رو جمع می‌زنه
# 2. محصول رو آپدیت می‌کنهsales_count
# 3. لیست پرفروش‌ها همیشه به‌روز می‌مونه!
# مثال:
# - 3 گوشی بفروشی → sales_count=3
# - 5 گوشی دیگه → sales_count=8 (اتومات)
SALE_WAREHOUSE_TYPE_ID = 2   # خروجی/فروش
@receiver(post_save, sender=Warehouse)
def update_product_sales_count(sender, instance, **kwargs):
    if instance.product and instance.warehouse_type_id == SALE_WAREHOUSE_TYPE_ID:
        total_sales= Warehouse.objects.filter(
            product = instance.product,
            warehouse_type_id = SALE_WAREHOUSE_TYPE_ID   # فقط فروش‌ها
        ).aggregate(total=Sum('quantity'))['total'] or 0
        instance.product.sales_count = total_sales
        instance.product.save(update_fields=['sales_count'])
