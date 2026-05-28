from decimal import Decimal
from apps.products.models import Product
import utils

class ShopCart:

    def __init__(self, request):
        self.session = request.session
        self.shop_cart = self.session.get('shop_cart', {})
        if self.shop_cart is None:
            self.shop_cart = {}
            self.session['shop_cart'] = self.shop_cart
        self.count = len(self.shop_cart)

    def add_to_shop_cart(self, product, qty):
        product_id = str(product.id)
        if product_id not in self.shop_cart:
            self.shop_cart[product_id] = {
                'qty': 0,
                'price': str(product.price),
                'final_price': str(product.get_price_by_discount())
            }
        self.shop_cart[product_id]['qty'] += int(qty)
        self.count = len(self.shop_cart)
        self.save()

    def delete_from_shop_cart(self, product):
        product_id = str(product.id)
        if product_id in self.shop_cart:
            del self.shop_cart[product_id]
        self.count = len(self.shop_cart)
        self.save()

    def update(self, product_id_list, qty_list):
        for i, product_id in enumerate(product_id_list):
            if product_id in self.shop_cart:
                self.shop_cart[product_id]['qty'] = int(qty_list[i])
        self.save()

    def __len__(self):
        return self.count
    def final_price(self):
        total_price = self.calc_total_price()
        order_final_price, delivery, tax = utils.price_by_delivery_tax(total_price)
        return order_final_price

    def save(self):
        self.session['shop_cart'] = self.shop_cart
        self.session.modified = True

    def __iter__(self):
        product_ids = self.shop_cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        temp = self.shop_cart.copy()
        for product in products:
            temp[str(product.id)]['product'] = product
        for item in temp.values():
            qty = item.get('qty', 1)
            item['quantity'] = qty
            item['price'] = Decimal(item['price'])
            item['final_price'] = Decimal(item['final_price'])
            item['total_price'] = item['final_price'] * qty

            yield item

    def calc_total_price(self):
        total = Decimal('0')
        for item in self.shop_cart.values():
            qty = item.get('qty', 1)
            total += Decimal(item['final_price']) * qty
        return total

    def clear(self):
        self.session['shop_cart'] = {}
        self.session.modified = True
        self.shop_cart = {}
        self.count = 0
