from django.urls import path
from . import views

app_name='payments'
urlpatterns = [
    path('zarinpal-payment/<int:order_id>/', views.ZarinpalPaymentView.as_view(), name='zarinpal_payment'),
    path('verify/', views.ZarinpalPaymentVerifyView.as_view(), name='zarinpal_payment_verify'),
    path('show-verify-message/<str:message>/', views.show_verify_message, name='show_verify_message'),
]
