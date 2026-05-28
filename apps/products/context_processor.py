from django.db.models import Count
from .models import ProductGroup

from apps.products.models import ProductGroup

def navbar_categories(request):
    # 3 تا گروه اصلی (دقیقاً مثل navbar.html)
    main_groups = ProductGroup.objects.filter(
        is_active=True,
        slug__isnull=False,
        group_parent=None  # والد نداره
    )[:3]  # فقط 3 تا (دیجیتال، پوشاک، غذایی)

    for group in main_groups:
        # هر گروه → 4 تا زیردسته
        group.children = ProductGroup.objects.filter(
            group_parent=group,
            is_active=True,
            slug__isnull=False
        )

        # هر زیردسته → 3 تا محصول
        for child in group.children:
            child.products = child.products_of_groups.filter(
                is_active=True
            )

    return {'main_groups': main_groups}


