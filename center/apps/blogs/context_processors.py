from .models import Post

# این فایل برای داده‌های مشترک بین تمام صفحات سایت است.
# مثلاً مقالات محبوب، منوها، سبد خرید، یا تنظیمات عمومی سایت.
# ها قابل دسترسی هست template تابع داخل این فایل به صورت خودکار در تمام
# view بدون نیاز به ارسال داده از
def blog_sidebar(request):
    popular_posts = Post.published.order_by('-views')[:10]  # محبوب‌ترین مقالات
    return {
        'popular_posts':popular_posts
    }
