from django.utils.text import slugify
from apps.products.models import Brand, ProductGroup, Product

def make_slugs_unique(model, field_name):
    items = model.objects.all()
    for item in items:
        slug = getattr(item, field_name)
        if not slug:
            slug = slugify(
                getattr(item, 'brand_title', None) or
                getattr(item, 'group_title', None) or
                getattr(item, 'product_name', None),
                allow_unicode=True
            )

        base_slug = slug
        n = 1
        while model.objects.filter(**{field_name: slug}).exclude(pk=item.pk).exists():
            slug = f"{base_slug}-{n}"
            n += 1

        if getattr(item, field_name) != slug:
            setattr(item, field_name, slug)
            item.save(update_fields=[field_name])

    print(f"همه اسلاگ‌های مدل {model.__name__} یونیک شدند!")
