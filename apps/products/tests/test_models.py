import pytest
from apps.products.models import Product
from apps.products.factories import BrandFactory, ProductFactory


# اینجا خود مدل و منطق داخل مدل را تست می‌کنی. تمرکز روی: فیلدها، متدهای مدل، رفتار دیتا بیس
# @pytest.mark.django_db
# def test_product_creation():
#     product = Product.objects.create(
#         product_name = "Test Product",
#         slug = "test-product",
#         price = 50000,
#         is_active = True
#     )
#     assert product.product_name == "Test Product"
#     assert product.price == 50000
#     assert product.is_active is True


# @pytest.mark.django_db
# def test_product_str():
#     product = Product.objects.create(
#         product_name = "Laptop",
#         slug = "laptop",
#         price = 80000000
#     )
#     assert str(product) == "Laptop"


# # بجای بالایی تمیزترش اینه که اینطوری بسازیم
# @pytest.mark.django_db
# def test_products_str():
#     product = ProductFactoryTest()
#     assert str(product) == product.product_name




@pytest.mark.django_db
def test_product_factory_creation():
    product = ProductFactory()

    assert product.id is not None
    assert product.product_name is not None
    assert product.price >= 1000000


@pytest.mark.django_db
def test_product_factory_creates_brand():
    product = ProductFactory()

    assert product.brand is not None
    assert product.brand.brand_title is not None



