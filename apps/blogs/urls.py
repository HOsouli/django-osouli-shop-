from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('category/<str:slug>/', views.group_posts, name='group_posts'),
    path('<str:slug>/', views.post_detail, name='post_detail'),
]
