from django.urls import path
from . import views

app_name='orders'
urlpatterns = [
    path('shop-cart/',views.ShopCartView.as_view(),name='shop_cart'),
    path('show-shop-cart/',views.show_shop_cart,name='show_shop_cart'),
    path('add-to-shop-cart/',views.add_to_shop_cart,name='add_to_shop_cart'),
    path('delete-from-shop-cart/',views.delete_from_shop_cart,name='delete_from_shop_cart'),
    path('update-shop-cart/',views.update_shop_cart,name='update_shop_cart'),
    path('status-of-shop-cart/',views.status_of_shop_cart,name='status_of_shop_cart'),
    path('create-order/',views.CreateOrderView.as_view(),name='create_order'),
    path('checkout-order/<int:order_id>/',views.CheckOutView.as_view(),name='checkout_order'),
    path('apply-coupon/<int:order_id>/',views.ApplyCoupon.as_view(),name='apply_coupon'),
    path('clear/', views.clear_session, name='clear_session'),
]

