from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)  # برای سطح دسترسی کاربران PermissionsMixin کلاس
from django.utils import timezone
from utils import FileUpload


class CustomUserManager(BaseUserManager):
    def create_user(self, mobile_number, password=None, **extra_fields):
        if not mobile_number:
            raise ValueError('شماره موبایل الزامی است')

        # نرمال‌سازی ایمیل اگر وجود داشته باشد
        if 'email' in extra_fields:
            extra_fields['email'] = self.normalize_email(extra_fields['email'])

        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(mobile_number, password, **extra_fields)


# ______________________________________________________________________________
class CustomUser(AbstractBaseUser, PermissionsMixin):
    mobile_number = models.CharField(max_length=11, unique=True, verbose_name='شماره موبایل')
    email = models.EmailField(max_length=100, blank=True, verbose_name='ایمیل')
    name = models.CharField(max_length=50, blank=True, verbose_name='نام')
    family = models.CharField(max_length=50, blank=True, verbose_name='نام خانوادگی')

    GENDER_CHOICES = (('M', 'مرد'), ('F', 'زن'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', blank=True, null=True)

    register_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['name', 'family']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.name} {self.family} ({self.mobile_number})'

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

# خط شماره 188 نوشتم که به پروژم بگم از این کاستوم یوزر خودم تبعیت کن نه یوزر پیش فرض جنگو روsettings.py باید این خط وجود داشته باشه:
# AUTH_USER_MODEL = 'accounts.CustomUser'
#
# بعد از تغییر مدل:
# makemigrations
# migrate
# createsuperuser

# ______________________________________________________________________________
class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, verbose_name='کاربر') # هر کاربر یه مشتریه که کلید اصلی هم هست
    phone_number = models.CharField(max_length=11, null=True, blank=True, verbose_name='شماره تماس ثابت')
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')
    file_upload = FileUpload('images', 'customer')
    image_name = models.ImageField(upload_to=file_upload.upload_to, null=True, blank=True, verbose_name='تصویر پروفایل')

    class Meta:
        verbose_name = 'مشتری'
        verbose_name_plural = 'مشتریان'

