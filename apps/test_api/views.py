from apps.products.models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from .Serializers import ProductSerializer
from CustomePermissions import CustomPermissionForProducts

# میگم درصورتی میتونی اجرا بشی که این کاستوم پرمیژن رو رعایت کرده باشی و میاد چک میکنه قبل از اینکه ای پی آی رو تولید کنه و نشون بده باید این پرمیژت وجود داشته باشه کسی داره این اجازه دسترسی رو که اول اینکه کاربر باشه دوم اینکه احراز هویت شده باشه و لاگ این کرده باشه AllProductsApi که به این تابع BasePermission درست میکنم توی ریشه پروژه از تابع CustomePermissions برای اینکه حرفه ای باشه یه ماژول به اسم
class AllProductsApi(APIView):
    permission_classes=[CustomPermissionForProducts]
    def get(self, request):
        products=Product.objects.filter(is_active=True).order_by('-published_date')
        self.check_object_permissions(request, products)
        ser_date=ProductSerializer(instance=products, many=True)
        return Response(data=ser_date.data)


