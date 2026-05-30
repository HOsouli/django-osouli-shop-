# پروژه Django - فروشگاه آنلاین

یک پروژه فروشگاه اینترنتی توسعه‌داده‌شده با جنگو که شامل مدیریت کاربران، محصولات، سفارش‌ها، پرداخت، تخفیف‌ها، جستجو، انبار و بخش محتوا (وبلاگ/آموزش) است.
این ریپازیتوری برای ارائه رزومه منتشر شده و اطلاعات حساس از کد جدا شده‌اند.

---

## امکانات اصلی
- **مدیریت کاربران:** سیستم احراز هویت و پروفایل کاربری.
- **مدیریت محصولات:** دسته‌بندی پیشرفته، ویژگی‌های کالا و نمایش جزئیات.
- **سبد خرید و سفارشات:** جریان کامل ثبت سفارش و مدیریت وضعیت خرید.
- **سیستم پرداخت:** یکپارچه‌سازی با درگاه‌های پرداخت.
- **تخفیف‌ها:** مدیریت کد تخفیف و جشنواره‌های فروش.
- **جستجو:** سیستم جستجوی محصولات.
- **تعامل کاربران:** ثبت نظر، امتیازدهی و لیست علاقه‌مندی‌ها.
- **مدیریت انبار:** کنترل موجودی کالاها در انبارها.
- **محتوا و اطلاع‌رسانی:** بخش وبلاگ، اخبار و صفحات ثابت (درباره ما، قوانین و...).

---

## ساختار اپلیکیشن‌ها (Modular Apps)
- `accounts` — مدیریت کاربران
- `blogs` — اخبار، آموزش و محتوای مرتبط
- `comment_scoring_favorites` — نظرات، امتیازدهی و علاقه‌مندی‌ها
- `discounts` — مدیریت تخفیف‌ها
- `main` — بخش اصلی و تنظیمات پایه
- `orders` — مدیریت سفارش‌ها و سبد خرید
- `pages` — صفحات ثابت (تماس با ما، قوانین و...)
- `payments` — مدیریت تراکنش‌های بانکی
- `products` — مدیریت کاتالوگ محصولات
- `search` — موتور جستجوی داخلی
- `test-api` — رابط‌های تست API
- `warehouses` — مدیریت موجودی انبار

---

## راهنمای نصب و راه‌اندازی

### ۱. ساخت و فعال‌سازی محیط مجازی (Windows)
```bash
python -m venv venv
venv\Scripts\activate
```


### ۲. نصب وابستگی‌ها
```bash
pip install -r requirements.txt
```

### ۳. تنظیم متغیرهای محیطی
برای اجرای پروژه، یک فایل `.env` در ریشه اصلی پروژه ایجاد کنید و متغیرهای محیطی لازم (مانند `SECRET_KEY`, `DATABASE_URL`, `DEBUG` و ...) را طبق نمونه زیر در آن قرار دهید:
```env
# Example .env structure:
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://user:password@host:port/dbname
```

### ۴. اعمال مهاجرت‌ها و ادمین
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### ۵. اجرای پروژه
```bash
python manage.py runserver
```
نکته: در محیط تولید، قبل از اجرا دستور زیر را برای تجمیع فایل‌های استاتیک اجرا کنید:
```bash
python manage.py collectstatic
```

---

### امنیت و احراز هویت

در این پروژه، امنیت کاربران و حفاظت از داده‌ها اولویت اصلی بوده و لایه‌های حفاظتی زیر پیاده‌سازی شده است:

*   **احراز هویت دو مرحله‌ای (OTP):** طراحی سیستم ثبت‌نام و بازیابی رمز عبور بر پایه کد تایید (OTP) پیامکی. کدهای تایید در **Redis Cache** با طول عمر محدود ذخیره می‌شوند.
*   **کنترل سطح دسترسی (Access Control):** مدیریت دسترسی با `LoginRequiredMixin` و کنترل هوشمند ورود با متد `dispatch`.
*   **مقابله با حملات CSRF:** استفاده از دکوراتور `ensure_csrf_cookie` در نقاط حساس برای جلوگیری از حملات Cross-Site Request Forgery.
*   **ذخیره‌سازی امن رمز عبور:** استفاده از مکانیزم هشینگ پیش‌فرض جنگو (`PBKDF2/Argon2`)؛ هیچ رمز عبوری به صورت متن خام ذخیره نمی‌شود.
*   **اعتبارسنجی داده‌ها:** استفاده از `cleaned_data` و مدیریت خطاهای هم‌زمانی با بلوک‌های `try-except` و `IntegrityError`.
*   **محرمانگی تنظیمات:** جداسازی کامل اطلاعات حساس با استفاده از متغیرهای محیطی در فایل `.env`.

---



### Preview (Screenshots)
در این بخش، تعدادی از تصاویر منتخب پروژه قرار داده شده است تا نمای کلی وب‌سایت فروشگاه اینترنتی و بخش‌های اصلی مانند صفحه اصلی، دسته‌بندی محصولات، لیست محصولات، جزئیات محصول، نظرات کاربران، سبد خرید، پنل کاربری، احراز هویت، بلاگ و همچنین پنل مدیریت (Admin Panel) نمایش داده شود.

#### User Interface (Client Side)

| Core Features | Product & Order Management | Content & User Interaction |
|---|---|---|
| ![Main Page](docs/screenshots/Capture7.PNG) | ![Advanced Filtering](docs/screenshots/Capture18.PNG) | ![Product Tabs](docs/screenshots/Capture9.PNG) |
| ![Product Details](docs/screenshots/Capture17.PNG) | ![Order Checkout](docs/screenshots/Capture20.PNG) | ![Blog Section](docs/screenshots/Capture29.PNG) |
| ![Shopping Cart](docs/screenshots/Capture14.PNG) | ![User Dashboard](docs/screenshots/Capture4.PNG) | ![Authentication](docs/screenshots/Capture30.PNG) |
| ![Registration](docs/screenshots/Capture22.PNG) | ![Mobile View](docs/screenshots/Capture19.PNG) | ![Registration](docs/screenshots/reg-screen.png) |


#### Admin Panel

| Dashboard | Management | Transactions |
|---|---|---|
| ![Admin Dashboard](docs/screenshots/Capture.PNG) | ![Product Management](docs/screenshots/Capture0.PNG) | ![Order Details](docs/screenshots/Capture1.PNG) |

#### Project Architecture

| File Structure |
|---|
| ![Project Structure](docs/screenshots/Capture15.PNG) |


## هدف پروژه
این ریپازیتوری جهت نمایش توانایی در پیاده‌سازی معماری تمیز در جنگو، مدیریت دیتابیس‌های فروشگاهی و توسعه یک فروشگاه اینترنتی به عنوان نمونه‌کار منتشر شده است.

