from django.shortcuts import render, redirect
from django.views import View
from .forms import (
    RegisterUserForm,
    VerifyRegisterForm,
    LoginUserForm,
    ChangePasswordForm,
    RememberPasswordForm,
    UpdateProfileForm,
)
from .models import CustomUser, Customer
from django.contrib import messages
import utils
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.cache import cache
from django.db import IntegrityError

# ______________________________________________________________________________________________
@method_decorator(ensure_csrf_cookie, name="dispatch")
class RegisterView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = RegisterUserForm()
        return render(request, "accounts_app/register.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            mobile = cd["mobile_number"]

            # اگر شماره از قبل ثبت شده
            if CustomUser.objects.filter(mobile_number=mobile).exists():
                messages.info(request, "اگر امکانش وجود داشته باشد، پیامک ارسال می‌شود.")
                return redirect("accounts:login")

            active_code = utils.generate_activation_code()

            if utils.send_activation_sms(mobile, active_code):
                cache_key = f"reg_{mobile}"
                cache.set(
                    cache_key,
                    {
                        "active_code": str(active_code),
                        "password": cd["password1"],
                    },
                    120,
                )
                print("REGISTER CODE:", active_code)


                request.session["mobile_verify"] = mobile
                request.session.pop("reset_password_mode", None)

                return redirect("accounts:verify")

            messages.error(request, "ارسال کد تایید ناموفق بود. لطفاً دوباره تلاش کنید.")

        return render(request, "accounts_app/register.html", {"form": form})



# ______________________________________________________________________________________________
class VerifyRegisterCodeView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not request.session.get("mobile_verify"):
            messages.error(request, "ابتدا درخواست کد تایید ثبت شود.")
            if request.session.get("reset_password_mode"):
                return redirect("accounts:remember_password")
            return redirect("accounts:register")

        form = VerifyRegisterForm()
        return render(request, "accounts_app/authentication.html", {"form": form})

    def post(self, request, *args, **kwargs):
        mobile = request.session.get("mobile_verify")
        entered_code = request.POST.get("active_code")
        reset_mode = request.session.get("reset_password_mode")

        if not mobile:
            messages.error(request, "جلسه شما منقضی شده است. دوباره تلاش کنید.")
            return redirect("accounts:remember_password" if reset_mode else "accounts:register")

        cache_key = f"reset_{mobile}" if reset_mode else f"reg_{mobile}"
        cached_data = cache.get(cache_key)

        if cached_data and entered_code == str(cached_data.get("active_code")):

            # حالت فراموشی رمز
            if reset_mode:
                request.session["user_session"] = {"mobile_number": mobile}
                cache.delete(cache_key)
                request.session.pop("mobile_verify", None)
                request.session.pop("reset_password_mode", None)
                return redirect("accounts:change_password")

            # حالت ثبت‌نام
            if CustomUser.objects.filter(mobile_number=mobile).exists():
                cache.delete(cache_key)
                request.session.pop("mobile_verify", None)
                request.session.pop("reset_password_mode", None)
                messages.error(request, "این شماره قبلاً ثبت‌نام شده است. وارد شوید.")
                return redirect("accounts:login")

            try:
                CustomUser.objects.create_user(
                    mobile_number=mobile,
                    password=cached_data["password"],
                )
            except IntegrityError:
                # اگر به هر دلیل race condition رخ داد
                pass

            cache.delete(cache_key)
            request.session.pop("mobile_verify", None)
            request.session.pop("reset_password_mode", None)

            auth_user = authenticate(request, username=mobile, password=cached_data["password"])
            if auth_user is None:
                # یعنی backend شما با mobile_number authenticate نمی‌کند
                messages.success(request, "ثبت‌نام انجام شد. لطفاً وارد شوید.")
                return redirect("accounts:login")

            login(request, auth_user)
            messages.success(request, "ثبت‌نام شما با موفقیت انجام شد.")
            return redirect("main:index")

        messages.error(request, "کد وارد شده اشتباه است یا زمان آن به پایان رسیده.")
        return redirect("accounts:verify")



# ______________________________________________________________________________________________
class LoginUserViwe(View):
    #  وقتی کاربر وارد شده دیگه نباید با وارد کردن آدرس یوآر ال تو صفحه جدید دوباره بیاد تو همون صفحه ورود که الان توش هست برای همین با تعریف کردن متد دیسپچ دیگه کاربر نمیتونه هرجا بره ادرس صفحه ورو رو بزنه
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = LoginUserForm()
        return render(request, "accounts_app/login.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data["mobile_number"], password=data["password"]
            )
            if user is not None:
                if not user.is_staff:
                    messages.success(request, "ورود با موفقیت انجام شد", "success")
                    login(request, user)
                    next_url = request.GET.get("next")
                    if next_url is not None:
                        return redirect(next_url)
                    else:
                        return redirect("main:index")
                else:
                    messages.error(
                        request, "شما از این صفحه نمی توانید ورود کنید", "warning"
                    )
                    return render(request, "accounts_app/login.html", {"form": form})
            else:
                messages.error(request, "اطلاعات وارد شده نامعتبر است", "danger")
                return render(request, "accounts_app/login.html", {"form": form})
        else:
            messages.error(request, "اطلاعات وارد شده نامعتبر است", "danger")
            return render(request, "accounts_app/login.html", {"form": form})


# ______________________________________________________________________________________________
class LogoutUserViwe(View):
    # def dispatch(self,request,*args,**kwargs):
    #     if request.user.is_authenticated:
    #         return redirect('main:index')
    #     return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        data_session = request.session.get("shop_cart", {})
        logout(request)
        request.session["shop_cart"] = data_session
        return redirect("main:index")


# ______________________________________________________________________________________________
class ChangePasswordView(View):
    def get(self, request, *args, **kwargs):
        # اگر کاربر وارد سیستم شده است، مستقیماً فرم تغییر رمز را نمایش بده
        if request.user.is_authenticated:
            form = ChangePasswordForm()
            # می‌توانید یک سشن موقت برای اطمینان بیشتر ایجاد کنید، هرچند شاید لازم نباشد
            # request.session["user_session_for_change_password"] = True
            return render(request, "accounts_app/change_password.html", {"form": form})
        else:
            # اگر کاربر وارد سیستم نشده است، به صفحه فراموشی رمز هدایت کن
            messages.error(request, "لطفاً ابتدا وارد حساب کاربری خود شوید یا رمز عبور خود را بازیابی کنید.", "warning")
            return redirect("accounts:remember_password") # یا "accounts:login" اگر اولویت ورود است

    def post(self, request, *args, **kwargs):
        # برای POST، همچنان به سشن یا کاربر وارد شده نیاز داریم
        if not request.user.is_authenticated:
            messages.error(request, "لطفاً ابتدا وارد حساب کاربری خود شوید.", "warning")
            return redirect("accounts:login")

        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = request.user # چون کاربر وارد شده است، مستقیماً از request.user استفاده می‌کنیم

            try:
                # تغییر رمز عبور کاربر وارد شده
                user.set_password(data["password1"])
                user.save()

                # --- پاکسازی سشن‌ها (اختیاری، چون دیگر نیازی به user_session برای این کار نیست) ---
                # request.session.pop("user_session", None)
                # request.session.pop("reset_password_mode", None)

                messages.success(request, "رمز عبور شما با موفقیت تغییر کرد. لطفاً دوباره وارد شوید.", "success")
                # بعد از تغییر رمز، بهتر است کاربر را به صفحه ورود هدایت کنیم تا دوباره لاگین کند
                return redirect("accounts:login")

            except Exception as e: # برای خطاهای احتمالی دیگر
                messages.error(request, f"خطایی در تغییر رمز عبور رخ داد: {e}", "danger")
                return render(request, "accounts_app/change_password.html", {"form": form})
        else:
            messages.error(request, "اطلاعات وارد شده معتبر نمی‌باشد.", "danger")
            # در صورت نامعتبر بودن فرم، باید دوباره رندر شود
            return render(request, "accounts_app/change_password.html", {"form": form})




# ______________________________________________________________________________________________
class RememberPasswordView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = RememberPasswordForm()
        return render(request, "accounts_app/remember_password.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = RememberPasswordForm(request.POST)
        if form.is_valid():
            mobile = form.cleaned_data["mobile_number"]

            if not CustomUser.objects.filter(mobile_number=mobile).exists():
                messages.error(request, "کاربری با این شماره یافت نشد.")
                return render(request, "accounts_app/remember_password.html", {"form": form})


            active_code = utils.generate_activation_code()
            print(active_code)

            if utils.send_activation_sms(mobile, active_code):
                cache_key = f"reset_{mobile}"
                cache.set(cache_key, {"active_code": str(active_code)}, 300)

                request.session["mobile_verify"] = mobile
                request.session["reset_password_mode"] = True

                messages.success(request, "کد تایید برای فراموشی رمز ارسال شد.")
                return redirect("accounts:verify")

            # اگر SMS ارسال نشد
            messages.error(request, "ارسال کد تایید ناموفق بود. لطفاً دوباره تلاش کنید.")

        return render(request, "accounts_app/remember_password.html", {"form": form})



# ______________________________________________________________________________________________
class UserPanelView(
    LoginRequiredMixin, View
):  # LoginRequiredMixin کاربری که لاگ این نیست اگر اقدام کنه میفرستتش صفحه ورود با اضافه کردن
    def get(self, request):
        user = request.user
        try:
            customer = Customer.objects.get(user=request.user)
            user_info = {
                "name": user.name,
                "family": user.family,
                "email": user.email,
                "phone_number": customer.phone_number,
                "address": customer.address,
                "image": customer.image_name,
            }
        except ObjectDoesNotExist:
            customer = None
            user_info = {"name": user.name, "family": user.family, "email": user.email}
        return render(request, "accounts_app/userpanel.html", {"user_info": user_info})


# ______________________________________________________________________________________________
@login_required
def show_last_orders(request):
    orders = Order.objects.filter(customer_id=request.user.id).order_by(
        "-register_date"
    )[
        :5
    ]  # برو سراغ جدول سفارش ها همه اردرها رو بیار فیلترش کن اونایی که کاستومر آیدیشون برابر باشه با آیدیه کاربری که لاگ اینه مرتبشون کن بر اساس آخر به اول مثلا (پنجتای آخر رو )
    return render(
        request, "accounts_app/partials/show_last_orders.html", {"orders": orders}
    )


# ______________________________________________________________________________________________
class UpdateProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user

        try:
            customer = Customer.objects.get(user=request.user)
            initial_dict = {
                "mobile_number": user.mobile_number,
                "name": user.name,
                "family": user.family,
                "email": user.email,
                "phone_number": customer.phone_number,
                "address": customer.address,
            }
            image_url = customer.image_name
        except ObjectDoesNotExist:
            initial_dict = {
                "name": user.name,
                "family": user.family,
                "email": user.email,
                "mobile_number": user.mobile_number,
            }
            image_url = None

        form = UpdateProfileForm(
            initial=initial_dict
        )  # برای فرم برای اینه که اون فرم برای ویرایش هست و کاربر قصد ویرایش داره که حتما حتما باید با یک دیکشنری پر کنم و بدم بهش اما اگه فرم خالی باشه یعنی داخل پرانتز کلاس فرم چیزی نزاریم یه فرم خالی بهمون میده فقط دقت کن که فیلدهاش باید دقیقا همون فیلدهای کلاس فرم باشه initial صفت
        return render(
            request,
            "accounts_app/update_profile.html",
            {"form": form, "image_url": image_url},
        )

    # post حالا کاربر که ویرایش انجام داد اطلاعات رو میگیرم با متد
    def post(self, request):
        form = UpdateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            user = request.user

            user.name = cd["name"]
            user.family = cd["family"]
            user.email = cd["email"]
            user.save()

            customer, created = Customer.objects.get_or_create(user=user)
            customer.phone_number = cd["phone_number"]
            customer.address = cd["address"]

            if cd.get("image"):
                customer.image_name = cd["image"]

            customer.save()

            messages.success(request, "ویرایش پروفایل با موفقیت انجام شد", "success")
            return redirect("accounts:userpanel")
        else:
            messages.error(request, "اطلاعات وارد شده معتبر نمی باشد", "danger")
            return render(request, "accounts_app/update_profile.html", {"form": form})



# ______________________________________________________________________________________________
@login_required
def show_user_payments(request):
    payments = Order.objects.filter(customer_id=request.user.id).order_by(
        "-register_date"
    )
    return render(
        request, "accounts_app/show_user_payments.html", {"payments": payments}
    )
