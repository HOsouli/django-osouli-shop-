from django.urls import path
from . import views

app_name='csf'
urlpatterns = [
    path('create-comment/<str:slug>/', views.CommentView.as_view(), name='create_comment'),
    path('add-score/', views.add_score, name='add_score'),
    path('add-to-favorite/', views.add_to_favorite, name='add_to_favorite'),
    path('user-favorite/', views.UserFavoriteView.as_view(), name='user_favorite'),
]
