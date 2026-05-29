from django import forms
from django.forms import ModelForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repassword", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ["mobile_number", "email", "name", "family", "gender"]

    # تابع اعتبار سنجی چک کردن پسورد 1 و 2
    def clean_password2(self):
        cd = self.cleaned_data
        pass1 = cd.get("password1")
        pass2 = cd.get("password2")
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("رمز عبور و تکرار آن یکسان نیست")
        return pass2

    # بعد ذخیرش کن set_password ولی من اولش میگم ذخیره نکن چون میخوام پسوردم رو هش کنم با متد  True که اگر ما دوباره نویسی کنیم سیومون جایگزین میشه که این سیو یه کامیت داره که مقدار پیش فرضش  save خودش یه تابع داره به نام  ModelForm
    def save(self, commit=True):
        user = super().save(commit=False)  # این باعث میشه یوزر سیو نشه
        user.set_password(
            self.cleaned_data["password1"]
        )  # پسورد رو اول هش کن بعد سیو کن
        if commit:
            user.save()
        return user

# ________________________________________________________________________________
class UserChangeForm(forms.ModelForm):
    password = (
        ReadOnlyPasswordHashField(help_text="برای تغییر رمز عبور <a href='../password'>کلیک</a> کنید")
    )  # این باعث میشه که پسورد داخل صفحه چنج فرممون بصورت ردانلی باشه همین و همین و اگر بخوایم اینو تغییر بدیم داخل باید اینو کلیک کنه

    class Meta:
        model = CustomUser
        fields = [
            "mobile_number",
            "password",
            "email",
            "name",
            "family",
            "gender",
            "is_active",
            'is_staff'
        ]
# ________________________________________________________________________________
class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField(label="رمز عبور", widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'رمز عبور'}))
    password2 = forms.CharField(label="تکرار رمز عبور", widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'تکرار رمز عبور'}))

    class Meta:
        model = CustomUser
        fields = ['mobile_number',]
        widgets = {
            'mobile_number': forms.TextInput(attrs={'class':'form-control','placeholder':'۰۹xxxxxxxxx'}),
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'نام'}),
            'family': forms.TextInput(attrs={'class':'form-control','placeholder':'نام خانوادگی'}),
        }

    def clean_mobile_number(self):
        mobile = self.cleaned_data.get('mobile_number')
        if not mobile.startswith('09') or len(mobile) != 11:
            raise ValidationError("شماره موبایل معتبر نیست.")
        return mobile

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password1') != cd.get('password2'):
            raise ValidationError("رمز عبور و تکرار آن مطابقت ندارند.")
        return cd.get('password2')
# ________________________________________________________________________________
class VerifyRegisterForm(forms.Form):
    active_code = forms.CharField(label='',error_messages={'required':'این فیلد نمی‌تواند خالی باشد'},
    widget=forms.TextInput(attrs={'class':'form-control','placeholder':'کد دریافتی را وارد کنید'})
    )
# ________________________________________________________________________________
class LoginUserForm(forms.Form):
    mobile_number = forms.CharField(label='شماره موبایل',error_messages={'required':'این فیلد نمی‌تواند خالی باشد'},
    widget=forms.TextInput(attrs={'class':'form-control','placeholder':'موبایل را وارد کنید'})
    )
    password = forms.CharField(label='رمز عبور',error_messages={'required':'این فیلد نمی‌تواند خالی باشد'},
    widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'رمز عبور را وارد کنید'})
    )
# ________________________________________________________________________________
class ChangePasswordForm(forms.Form):
    password1=forms.CharField(label='', error_messages={'required':'این فیلد نمی تواند خالی باشد'},
    widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'رمز عبور را وارد کنید'})
    )
    password2=forms.CharField(label='', error_messages={'required':'این فیلد نمی‌تواند خالی باشد'},
    widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'تکرار رمز عبور را وارد کنید'})
    )
    def clean_password2(self):
        cd = self.cleaned_data
        pass1 = cd.get("password1")
        pass2 = cd.get("password2")
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("رمز عبور و تکرار آن یکسان نیست")
        return pass2

# ________________________________________________________________________________
class RememberPasswordForm(forms.Form):
    mobile_number=forms.CharField(label='', error_messages={'required':'این فیلد نمی تواند خالی باشد'},
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'موبایل را وارد کنید'})
    )

# ________________________________________________________________________________
class UpdateProfileForm(forms.Form):
    mobile_number=forms.CharField(
        label="",
        error_messages={'required':'این فیلد نمیتواند خالی باشد'},
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'شماره موبایل را وارد کنید','readonly':'readonly'})  # تو ویجتم بنویسم "readonly:readonly" چون معیار یونیک بودن سیستم من شماره موبایل کاربرام هست و فیلدی از فرم که نباید تغییر کنه حتما باید از
    )
    name=forms.CharField(
        label="",
        error_messages={'required':'این فیلد نمیتواند خالی باشد'},
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام خود را وارد کنید'})
    )
    family=forms.CharField(
        label="",
        error_messages={'required':'این فیلد نمیتواند خالی باشد'},
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'نام خانوادگی خود را وارد کنید'})
    )
    email=forms.CharField(
        label="",
        error_messages={'required':'این فیلد نمیتواند خالی باشد'},
        widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'ایمیل خود را وارد کنید'})
    )
    phone_number=forms.CharField(
        label="",
        error_messages={'required':'این فیلد نمیتواند خالی باشد'},
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'تلفن ثابت خود را وارد کنید'})
    )
    address=forms.CharField(
        label="",
        error_messages={'required':'این فیلد نمیتواند خالی باشد'},
        widget=forms.Textarea(attrs={'class':'form-control','placeholder':'آدرس خود را وارد کنید'})
    )
    image=forms.ImageField(required=False)
