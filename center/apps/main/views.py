from django.shortcuts import render
from django.conf import settings
from django.views import View
from .models import Slider
from django.utils import timezone
from apps.products.models import ProductGroup

def media_admin(request):
    return {'media_url':settings.MEDIA_URL,}

# _________________________________________________________________________
def index(request):
    sliders = Slider.objects.filter(is_active=True, published_date__lte=timezone.now())

    product_groups = ProductGroup.objects.filter(
        is_active=True,
        slug__isnull=False
    )[:12]  # بدون order_by!

    return render(request, 'main_app/index.html', {
        'sliders': sliders,
        'product_groups': product_groups
    })

# _________________________________________________________________________
class SliderView(View):
    def get(self, request):
        sliders=Slider.objects.filter(is_active=True, published_date__lte=timezone.now())
        return render(request, "main_app/sliders.html",{'sliders':sliders})

# _________________________________________________________________________
def handler404(request, exception=None):
    return render(request, 'main_app/404.html')


