from django.shortcuts import render, get_object_or_404
from .models import StaticPage

def about_us(request):
    page = get_object_or_404(StaticPage, page_type='about', is_active=True)
    return render(request, 'pages_app/about_us.html', {'page': page})

def contact_us(request):
    page = get_object_or_404(StaticPage, page_type='contact', is_active=True)
    return render(request, 'pages_app/contact_us.html', {'page': page})

def rules(request):
    page = get_object_or_404(StaticPage, page_type='rules', is_active=True)
    return render(request, 'pages_app/rules.html', {'page': page})


