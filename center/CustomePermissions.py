from rest_framework.permissions import BasePermission

# که اونجا ایمپورتش کردم این تابع برای چک کردن اینه که ببینه کسی که اینو صدا زده کاربر هست احراز هویت کرده بوده از قبل یعنی لاگ این بوده یا نه که داره از این ای پی آی استفاده میکنه اگر کاربر هست اجازه دسترسی بهش بدم test_api برای ویو
class CustomPermissionForProducts(BasePermission):
    def has_permission(self, request, obj):
        return request.user and request.user.is_authenticated
