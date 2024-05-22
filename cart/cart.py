from decimal import Decimal
from django.conf import settings
from construct_site_food.models import Good


class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        good_ids = self.cart.keys()
        cart = self.cart.copy()
        for item in cart.values():
            item['id'] = str(item['id'])
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def add(self, product, quantity=1, decrement=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'id': product_id, 'quantity': 0,
                                     'price': str(product.price)}
        if decrement:
            self.cart[product_id]['quantity'] -= quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        if self.cart[product_id]['quantity'] <= 0:
            del self.cart[product_id]
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_items(self):
        quantity = 0
        return sum(item['quantity'] for item in self.cart.values())

    def get_good(self, good):
        good_id = str(good.id)
        if good_id in self.cart:
            return self.cart[good_id]
        return False

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_good_ids(self):
        return self.cart.keys()

