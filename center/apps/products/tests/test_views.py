import pytest
from django.urls import reverse
from apps.products.models import Product
from apps.products.factories import ProductFactory, BrandFactory


# # در اینجا رفتارهای ویو و صفحات را تست می‌کنیم، شامل وضعیت پاسخ، داده‌ی رندر شده و صفحه‌بندی
# @pytest.mark.django_db
# def test_products_page(client):
#     url = reverse("products:last_products")
#     response = client.get(url)

#     assert response.status_code == 200



# @pytest.mark.django_db
# def test_product_detail_view(client):
#     product = Product.objects.create(
#         product_name = "Mobile",
#         slug = "mobile",
#         price = 50000000
#     )
#     url = reverse("products:product_details", args=[product.slug])
#     response = client.get(url)

#     assert response.status_code == 200



# @pytest.mark.django_db
# def test_product_creation():
#     product = ProductFactory()

#     assert product.id is not None



# ساخت چند محصول با یک
@pytest.mark.django_db
def test_products_pagination(client):
    products = ProductFactory.create_batch(50)   # باید 50 محصول دستی بسازم factory مرتب‌سازی بدون pagination خط فرض کن بخواهی تست کنی: فیلتر قیمت یا فیلتر برند یا
    response = client.get("/products/")  # درخواست به صفحه محصولات

    assert response.status_code == 200  # وضعیت باید درست باشد
    assert len(products) == 50   # مطمئن می‌شویم تعداد محصولات ساخته شده درست است



@pytest.mark.django_db
def test_products_list_page(client):
    brand = BrandFactory()  # یک Brand می‌سازد
    ProductFactory.create_batch(5, brand=brand)  # محصولات را به آن برند ارجاع بده
    url = reverse("products:items", kwargs={"slug":brand.slug})
    response = client.get(url)

    assert response.status_code == 200

