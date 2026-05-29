from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from apps.products.models import Product

class SearchResultsView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')  # دادم تو نوبار هم خط 189 کیو دادم و تو هدر هم نوشتم خط 40 دوتا سرچ هست تو وب q ش رو هم برابر با همین میدیم که اینجا من name هرچی اینجا تعریف کنی برای جستجو باید تو اچ تی ام ال
        products = Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(description__icontains=query)
        )
        context = {
            "products": products,
        }
        return render(request, 'search_app/search_results.html', context)

