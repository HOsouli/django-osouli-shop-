import django_filters
from .models import Product,Brand,FeatureValue

# باشه django_filters.FilterSet برای فیلتر باید کلاسی بنویسیم که فرزند
# مثلا برای برند و قیمت و گروه کالا یا هرچیزی فیلتر بنویسی و بر اساس نوعی که میخوای فیلتر کنی باید صدا بزنی نوعش رو دقیقا عین مدل ها
class ProductFilter(django_filters.FilterSet):
    price=django_filters.NumberFilter(field_name='price', lookup_expr='lte')   # که بهش میگی مثلا کوچکتر از یا بزرگتر از یا کوچکتر و مساویه اون نام فیلد مثلا قیمت باشه lookup_expr یه نام فیلد میگیره یه صفتی به اسم
    brand=django_filters.ModelMultipleChoiceFilter(field_name='brand', queryset=Brand.objects.all())
    feature=django_filters.ModelMultipleChoiceFilter(field_name='features', queryset=FeatureValue.objects.all())  # relation به FeatureValue
