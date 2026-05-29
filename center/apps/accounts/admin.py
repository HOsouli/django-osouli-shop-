from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserChangeForm, UserCreationForm
from .forms import CustomUser
from .models import CustomUser,Customer


class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('mobile_number', 'email', 'name', 'family', 'gender', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'family')
    search_fields = ('mobile_number', 'family')
    ordering=('mobile_number',)     # مرتب سازی بر اساس شماره موبایل

    # فیلد ست من اینا باشهchangeform وقتی رفتی تو قسمت
    fieldsets = (
        (None, {'fields': ('mobile_number', 'password')}),
        ('اطلاعات شخصی', {'fields': ('name', 'family', 'email', 'gender')}),
        ('دسترسی‌ها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('تاریخ‌ها', {'fields': ('last_login', 'register_date')}),
    )

    # یعنی موقع ادد کردن اینارو بیاریم addform اینم قسمت
    add_fieldsets=(
        (None,{
            'classes': ('wide',),
            'fields':('mobile_number', 'email', 'name', 'family', 'gender', 'password1', 'password2')}),
    )

    filter_horizontal=('groups', 'user_permissions')

admin.site.register(CustomUser, CustomUserAdmin)    # CustomUserAdmin رو به کمک CustomUser برای من ریجیستر کن مدل


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
