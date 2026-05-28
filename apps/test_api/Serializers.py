from rest_framework import serializers
from apps.products.models import Product

# ریشه یا همون اصلی پروژه هم آدرسش رو بدم که اینکارارو کردم urls.py اپلیکیشن هم مثل همیشه آدرسش رو بدم و بعد توی  urls.py برای ساختن ای پی آی اولین کار داده هایی که میخوایم رو سریالایزش میکنم بعد تو ویو واکشی میکنیم که بصورت سریالایزی (جیسان) نمایش بده بهمون و برای اینکه نشونمون بده قاعدتا باید تو
# اینو میدیم به کسی که سمت فرانت و ازش استفاده کنه داده های من رو نشون بده مثلا کسی که ری اکت کاره یا جاوا اسکرسپت کاره test_api/products ودر نهایت ای پی آی من میشه
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields = "__all__"
