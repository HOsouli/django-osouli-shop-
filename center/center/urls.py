"""
URL configuration for center project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('control-center-z7/', admin.site.urls),
    path('', include('apps.main.urls',namespace='main')),
    path('accounts/', include('apps.accounts.urls',namespace='accounts')),
    path('products/', include('apps.products.urls',namespace='products')),
    path('orders/', include('apps.orders.urls',namespace='orders')),
    path('discounts/', include('apps.discounts.urls',namespace='discounts')),
    path('payments/', include('apps.payments.urls',namespace='payments')),
    path('warehouses/', include('apps.warehouses.urls',namespace='warehouses')),
    path('csf/', include('apps.comment_scoring_favorites.urls',namespace='csf')),
    path('search/', include('apps.search.urls',namespace='search')),
    path('pages/', include('apps.pages.urls',namespace='pages')),
    path('blogs/', include('apps.blogs.urls', namespace="blogs")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('test_api/', include('apps.test_api.urls', namespace='test_api')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# هم نوشتم و توضیح دادم main خط 30 دادم که چه موقعی این تابع ها رو مینویسیم تابعش هم تو ویو settings.py این تابع رو تو همین آدرس نوشتمم توضیحاتش رو که برای چیه وزمانیکه اینو مینویسیم هم توضیحش رو هم تو
handler404 = 'apps.main.views.handler404'
