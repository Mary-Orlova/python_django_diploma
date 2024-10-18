from django.shortcuts import get_object_or_404
from rest_framework import permissions

from catalog.models import Product
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from cart.cart import Cart
from cart.serializers import BasketSerializer


def get_products_in_cart(cart):
    """Товары в корзине"""
    products_in_cart = [product for product in cart.cart.keys()]
    products = Product.objects.filter(pk__in=products_in_cart)
    serializer = BasketSerializer(products, many=True, context=cart.cart)
    return serializer


class BasketView(APIView):
    """Корзина: получение, добавление и удаления продуктов"""
    # permission_classes = [permissions.IsAuthenticated]
    # если раскомментировать строчку выше - не авторизованный пользователь не сможет добавлять в корзину товары
    # Сейчас корзина хранится в сессии и при авторизации товары переносятся в корзину пользователя


    def get(self, *args, **kwargs) -> Response:
        "Метод получения данныз-товаров корзины"
        cart = Cart(self.request)
        serializer = get_products_in_cart(cart)
        return Response(serializer.data)

    def post(self, *args, **kwargs) -> Response:
        "Метод отравки данных-товаров корзины"
        cart = Cart(self.request)
        product = get_object_or_404(Product, id=self.request.data.get('id'))
        cart.add(product=product, count=self.request.data.get('count'))
        serializer = get_products_in_cart(cart)
        return Response(serializer.data)

    def delete(self, *args, **kwargs) -> Response:
        """Метод удаления товаров из корзины"""
        cart = Cart(self.request)
        product = get_object_or_404(Product, id=self.request.data.get('id'))
        count = self.request.data.get('count', False)
        cart.remove(product, count)
        serializer = get_products_in_cart(cart)
        return Response(serializer.data)
