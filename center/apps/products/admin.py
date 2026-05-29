from django.contrib import admin
from.models import Brand,ProductGroup,Product,ProductFeature,Feature,ProductGallery, FeatureValue
from django.db.models.aggregates import Count
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Q
from django.contrib.admin import SimpleListFilter   # فیلتر کردن بر اساس چیزی که خودمون میهوایم مثلا فیلتر کردن بر اساس والد که تو خط 53 نوشتم
from django_admin_listfilter_dropdown.filters import DropdownFilter   # و به لیست فیلتر هم اضافه شه که من جفتش رو انجام دادم installed_appa هم باید اضافه شه قسمت settings.py بعد از نصب خط شماره 124 رو از کامنت دربیار بجای خط 123 استفاده گن و تو
from admin_thumbnails import thumbnail
from import_export.admin import ExportMixin   # حالا تو پنل Admin دکمه Export اضافه میشه و میتونی فایل CSV/Excel خروجی بگیری یا حتی import کنی.
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from django.utils.text import slugify

# _____________________________________________________________________________

class EntityAdmin(admin.ModelAdmin):
    ...
    list_filter = (
        # for ordinary fields
        ('a_charfield', DropdownFilter),
        # for choice fields
        ('a_choicefield', ChoiceDropdownFilter),
        # for related fields
        ('a_foreignkey_field', RelatedDropdownFilter),
    )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_title','slug')
    list_filter = ('brand_title',)
    search_fields = ('brand_title',)
    ordering = ('brand_title',)
    readonly_fields = ('slug',)


# آپدیت نویسی یا همون اکشن نویسی
# actions یه طور مثال میخوام عملیات غیر فعال سازی بنویسم که حتما حتما سه تا ورودیهایی که نوشتم رو میخواد و در آخر باید اسم این تابع رو بزارم تو
def de_active_product_group(modeladmin, request, queryset):
    res=queryset.update(is_active=False)
    message=f'تعداد {res} کالا غیر فعال شد'
    modeladmin.message_user(request, message)
    # وقتی که عملیات اکشن اتفاق افتاد میتونیم بجای اون پیغام انگلیسی موفقیت آمیز رو به فارسی تبدیلش کنیم مثلا میریزیم تو یه ظرفی و نسبت به اون مقدار پیام بده غیر فعال شد

# و تابع فعال کردنشون
def active_product_group(modeladmin, request, queryset):
    res=queryset.update(is_active=True)
    message=f'تعداد {res} کالا فعال شد'
    modeladmin.message_user(request, message)

# و یا خروجی گرفتن به روش جیسانی
def export_json(modeladmin, request, queryset):
    response=HttpResponse(content_type='application/json')   #  پاسخم از نوع اپلیکیشن جیسانی باشه
    serializers.serialize('json', queryset, stream=response)
    return response


# ==========================================================
# استفاده کینم که باعث میشه بصورت عمودی فرزندانش رو زیر خودش  نشون بده برای اد کردن تو پنل ادمین TabularInline زمانی که کلاسی که تو ادمین تعریف میکنیم که از مدلی که کلید خارجی داره میتونیم از
class ProductGroupInstanceInlineAdmin(admin.TabularInline):
    model = ProductGroup
    fk_name = 'group_parent'
    extra = 6   # میتونم تو قسمت اد کردن اون پایین قسمت عنوان گروه کالا که بصورت پیشفرض 3 تا هست رو هر عددی بدیم همون تعداد عنوان گروه کالا رو میارهextra به کمک

# ==========================================================
# list_filter فیلتر کردن بر اساس والد، سمت راست پنل ادمین (گروه هایی که خودشون والد هستن) یه کلاس تعریف میکنم و به کمک ماژول سیمپل لیست فیلتر. وقتی این کلاس تعریف شد میتونم اسم این کلاس رو بزارم تو
class GroupFilter(SimpleListFilter):
    title = 'گروه محصولات'   # نامگزاری عنوان فیلتر سمت راست پنل ادمین
    parameter_name='group'  # group تو آدرس یوآرال میاد چون به گروه ربط داره من نوشتم group باعث میشه وقتی به والدشون تو قسمت فیلترها سمت راست پنل ادمین کلیک میکنم رکورد فرزندانشون رو نشون بده حالا مقدارش رو هرچیز دلخواهی میشه گذاشت درواقع این

    # میتونم با دوباره نویسی این تابع جایگزین کنم و فیلترمون رو عوض کنیم این تابع اجباریه پیاده سازیش تا بتونیم از کوئری ست تغییرات بگیریمlookups استفاده میکنیم این کلاس یه تابع داره به اسم SimpleListFilter زمانیکه از کلاس
    def lookups(self, request, model_admin):
        sub_groups=ProductGroup.objects.filter(~Q(group_parent=None))  # اونهایی که والد دارن رو برای من پیدا کن ساپ گروپ درواقع لیست تمام گروه هایی که والد دارن
        groups=set([item.group_parent for item in sub_groups])  # گروه هایی که والد دارن برو والد هاشون رو بکش بیرون
        return [(item.id, item.group_title) for item in groups]  # این گروه ها رو آیدی ها و عنوان گروهشون رو برگردون

# مثلا که وقتی سمت راست قسمت فیلتر ها رو یکی از والد ها کلیک میکنم تو قسمت آدرس یوآرال اون آی دیه مرتبط با اون والد رو میاره از دیتا بیس و فرزندانش رو نشون میده group=20 که این ولیو همون آی دی میشه که تو یوآرال آخر آدرس میزنه  value اشاره داره به queryset این تابع
    def queryset(self, request, queryset):
        if self.value()!=None:
            return queryset.filter(Q(group_parent=self.value()))
        return queryset  # میشه all در غیر این صورت همشون روبیار همون تو قسمت فیلتر گزینه


# ==========================================================
@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ('group_title','is_active','group_parent','slug','register_date','update_date','count_sub_group','count_product_of_group')
    list_filter = (GroupFilter,'is_active')
    search_fields = ('group_title',)
    ordering = ('group_parent','group_title',)
    inlines = [ProductGroupInstanceInlineAdmin]
    actions = [de_active_product_group, active_product_group, export_json]
    list_editable = ['is_active',]
    readonly_fields = ('slug',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('slug',)
        return ()

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            base_slug = slugify(obj.group_title, allow_unicode=True)
            slug = base_slug
            n = 1
            while ProductGroup.objects.filter(slug=slug).exclude(pk=obj.pk).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            obj.slug = slug
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # فقط گروه‌های والد رو نشون بده
        qs = qs.filter(group_parent__isnull=True)
        # شمارش زیر گروه‌ها و محصولات
        qs = qs.annotate(sub_group=Count('groups'))
        qs = qs.annotate(product_of_group=Count('products_of_groups'))
        return qs

    def count_sub_group(self, obj):
        return getattr(obj, 'sub_group', 0)

    def count_product_of_group(self, obj):
        return getattr(obj, 'product_of_group', 0)

    count_sub_group.admin_order_field = 'sub_group'
    count_sub_group.short_description = 'تعداد زیر گروه ها'
    count_product_of_group.short_description = 'تعداد کالاهای گروه'

    de_active_product_group.short_description = 'غیر فعال کردن گروه های انتخاب شده'
    active_product_group.short_description = 'فعال کردن گروه های انتخاب شده'
    export_json.short_description = 'خروجی json از گروه های انتخاب شده'



# _____________________________________________________________________________
class FeatureValueInline(admin.TabularInline):
    model=FeatureValue
    extra=6
# _____________________________________________________________________________
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('feature_name','display_groups','display_feature_values')
    list_filter = ('feature_name',)
    search_fields = ('feature_name',)
    ordering = ('feature_name',)
    inlines = [FeatureValueInline]

    # اضافه شن تا نمایش بده تو پنل ادمین list_display این دوتا تابع فقط برای نمایش توی پنل ادمینه که باید به
    # اسم گروه‌های کالایی که این ویژگی بهشون وصل شده رو کنار هم نشون میده
    def display_groups(self, obj):
        return ', '.join([group.group_title for group in obj.product_group.all()])

    # مقادیر مربوط به این ویژگی (مثل رنگ، سایز، وزن و …) رو به صورت خوانا نشون می‌ده
    def display_feature_values(self, obj):
        return ', '.join([feature_value.value_title for feature_value in obj.feature_values.all()])

    display_groups.short_description = 'گروه های دارای این ویژگی'
    display_feature_values.short_description = 'مقادیر برای این گروه'
# _____________________________________________________________________________
@admin.register(FeatureValue)
class FeatureValueAdmin(admin.ModelAdmin):
    list_display=('value_title', 'feature')
    search_fields=('value_title',)

# _____________________________________________________________________________
def de_active_product(modeladmin, request, queryset):
    res=queryset.update(is_active=False)
    message=f'تعداد {res} کالا غیر فعال شد'
    modeladmin.message_user(request, message)

def active_product(modeladmin, request, queryset):
    res=message=queryset.update(is_active=True)
    message=f'تعداد {res} کالا فعال شد'
    modeladmin.message_user(request, message)

class ProductFeatureInlineAdmin(admin.TabularInline):
    model = ProductFeature
    extra = 3

    class Media:
        js = ('js/admin_script.js',)


class ProductGalleryInlineAdmin(admin.TabularInline):
    model = ProductGallery
    extra = 3


@thumbnail('image_name')  # نام فیلد تصویر
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','brand','is_active','update_date','slug','display_product_group')
    list_filter = (('brand__brand_title',DropdownFilter),('product_group__group_title',DropdownFilter),'is_active')
    search_fields = ('product_name',)
    ordering = ('update_date','product_name',)
    actions=[de_active_product,active_product]
    inlines=[ProductFeatureInlineAdmin,ProductGalleryInlineAdmin]
    list_editable=['is_active']
    readonly_fields = ('slug',)

    de_active_product.short_description='غیر فعال کردن کالاهای انتخاب شده'
    active_product.short_description='فعال کردن کالاهای انتخاب شده'

    # تابعی برای ساختن یه ستون برای نشون دادن کالایی که بدونیم جزء چه گروهیه
    def display_product_group(self, obj):   # به هرکدوم از رکوردها (کالاها) اشاره داره obj این
        return ', '.join([group.group_title for group in obj.product_group.all()])   # تمام گروه هایی که یه کالا داره عنوان گروه هاشون رو نشون بده


    display_product_group.short_description='گروه های کالا'

# نکته: به طور مثال پیراهن جزء پوشاک مردانه یا زنانه هست دیگه درست نیست تو قسمت گروه کالا تو پنل ادمین اون قسمت که میخوایم گروهشون رو اد کنیم یا تغییر بدیم معنی نداره مد و پوشاک هم باشه
# هست اینکارو میکنم formfield_for_manytomany به اسم ModelAdmin به همین دلیل از تو قسمت اد، مد و پوشاک که میشه ریشه گروه رو از اون قسمت حذف میکنیم که به وسیله تابعش تو کلاس
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'product_group':
            # فقط گروه‌های فرزند + گروه‌هایی که محصول فعلی بهشون وصل شده
            if request.resolver_match.kwargs.get('object_id'):
                product_id = request.resolver_match.kwargs.get('object_id')
                product = Product.objects.get(pk=product_id)
                kwargs['queryset'] = ProductGroup.objects.filter(
                    Q(group_parent__isnull=False) | Q(products_of_groups=product)
                )
            else:
                kwargs['queryset'] = ProductGroup.objects.filter(group_parent__isnull=False)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


# fieldsets برای اینکه بخوایم پنل ادمین رو از شلوغی در بیاریم میتونیم بعضی از فیلد هامون رو که جای زیادی نمیگیره به افقی تبدیل کنیم به کمک
fieldsets = (
    ('اطلاعات محصول', {
        'fields': (
            'product_name',
            'image_name',
            'description',
            'slug',
        )
    }),
    ('گروه و برند', {
        'fields': (
            'product_group',
            ('brand', 'is_active'),
        )
    }),
    ('تاریخ و زمان', {
        'fields': (
            'published_date',
        )
    }),
)

# _____________________________________________________________________________
