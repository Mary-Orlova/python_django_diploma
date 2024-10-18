from decimal import Decimal
from django.conf import settings
from catalog.models import Product


class Cart(object):
    """Корзина"""
    def __init__(self, request):
        """Создание сессии корзины"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            # cохранение пустую корзину в сеансе
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, count):
        """Добавить продукт в корзину или обновить его количество"""
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {'count': count,
                                     'price': str(product.price)}
        else:
            self.cart[product_id]['count'] += count
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product, count):
        """Удаление товара из корзины."""
        product_id = str(product.id)
        if product_id in self.cart:
            if self.cart[product_id]['count'] > 1:
                if self.cart[product_id]['count'] == count:
                    del self.cart[product_id]
                else:
                    self.cart[product_id]['count'] -= 1
            else:
                del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Перебор элементов в корзине и получение продуктов из базы данных"""
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['count']
            yield item

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def total_count(self):
        """Количество товаров в корзине"""
        return sum(item['count'] for item in self.cart.values())

    def total_price(self):
        """Общая стоимость товаров в корзине"""
        return sum(Decimal(item['price']) * item['count'] for item in self.cart.values())
