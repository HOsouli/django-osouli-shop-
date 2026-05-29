from django.urls import path
from . import views

app_name='products'
urlpatterns = [
    path("search/", views.ProductSearchView.as_view(), name="search"),
    path('cheapest-products/', views.get_cheapest_products,name='cheapest_products'),
    path('last-products/', views.get_last_products,name='last_products'),
    path('top-selling-products/', views.get_top_selling_products, name='top_selling_products'),
    path('popular-product-groups/', views.get_popular_product_groups,name='popular_product_groups'),
    path('product-details/<str:slug>/', views.ProductDetailView.as_view(),name='product_details'),  # اضافه شه a تو تگ  products_box.html محصولاتی رو که نشون میدم هر محصولی قابل کلیکه هرکدوم یه تگ ای داره اچ رف داره میگم روی عکسش که کلیک میشه بره به این آدرس که تابعش رو نوشتم تو ویو و باید تو
    path('related-products/<str:slug>/', views.get_related_products,name='related_products'),
    path('product-groups/', views.ProductGroupsView.as_view(),name='product_groups'),
    path('items/<str:slug>/', views.ProductsByGroupView.as_view(),name='items'),
    path('ajax-admin/', views.get_filter_value_for_feature,name='filter_value_for_feature'),
    path('product-groups-partial/', views.get_products_group,name='product_groups_partial'),
    path('brand-partial/<str:slug>/', views.get_brands,name='brand_partial'),
    path('features-for-filter/<str:slug>/', views.get_features_for_filter,name='features_for_filter'),
    path('compare/', views.ShowCompareListView.as_view(), name='compare_list'),
    path('compare-table/', views.compare_table,name='compare_table'),
    path('add-to-compare-list/', views.add_to_compare_list,name='add_to_compare_list'),
    path('delete-from-compare-list/', views.delete_from_compare_list,name='delete_from_compare_list'),
    path('status-of-compare-list/', views.status_of_compare_list, name='status_of_compare_list'),
]
