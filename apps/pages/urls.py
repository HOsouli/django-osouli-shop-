from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path('about-us/', views.about_us, name='about-us'),
    path('contact-us/', views.contact_us, name='contact-us'),
    path('rules/', views.rules, name='rules'),
]
