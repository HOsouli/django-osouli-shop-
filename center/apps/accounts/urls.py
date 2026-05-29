from django.urls import path
from . import views

app_name='accounts'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify/', views.VerifyRegisterCodeView.as_view(), name='verify'),
    path('login/', views.LoginUserViwe.as_view(), name='login'),
    path('logout/', views.LogoutUserViwe.as_view(), name='logout'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('remember-password/', views.RememberPasswordView.as_view(), name='remember_password'),
    path('userpanel/', views.UserPanelView.as_view(), name='userpanel'),
    path('show-last-orders/', views.show_last_orders, name='show_last_orders'),
    path('show-user-payments/', views.show_user_payments, name='show_user_payments'),
    path('update-profile/', views.UpdateProfileView.as_view(), name='update_profile'),
]

