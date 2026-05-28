import factory
from .models import Product,Brand

# class ProductFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Product

#     product_name = factory.Faker("word")   # استفاده میشه factory خودش مقدار نیست؛ فقط می‌گوید یک کلمه تصادفی تولید کن توی "word"
#     slug = factory.Faker("slug")
#     price = 1000000
#     is_active = True



# class ProductFactoryTest(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Product

#     product_name = factory.Faker("sentence", nb_words=3)  # برای اسم های تصادفی چند کلمه ای استفاده میشه توی تست گرفتن مثلا اینجا گفتم 3 کلمه ای باشه نام محصول nb_words از
#     slug = factory.Faker("slug")
#     description = factory.Faker("sentence")
#     price = factory.Faker("random_int", min=1000000, max=5000000)
#     is_active = True



# هم ساخته میشود Brand ساخته شود Product وقتی
class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    brand_title = factory.Faker("company")
    slug = factory.Faker("slug")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    product_name = factory.Faker("word")
    price = factory.Faker("random_int", min=1000000, max=6000000)
    brand = factory.SubFactory(BrandFactory)


# __________________________________________________________________

