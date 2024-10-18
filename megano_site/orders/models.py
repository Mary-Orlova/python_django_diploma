"""Модели Заказов и оплаты"""

from django.contrib.auth.models import User
from django.db import models
from catalog.models import Product


class Order(models.Model):
    """Модель заказов товаров"""
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    id = models.AutoField(primary_key=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    fullName = models.CharField(max_length=40, blank=True)
    email = models.CharField(max_length=40, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    deliveryType = models.CharField(max_length=100, default='',)
    paymentType = models.CharField(max_length=20, blank=True)
    totalCost = models.DecimalField(max_digits=8, default=1, decimal_places=2,)
    status = models.CharField(max_length=100, default='', )
    city = models.CharField(max_length=40, default='', blank=True)
    address = models.CharField(max_length=200, default='', blank=True)
    products = models.ManyToManyField(Product, related_name='orders', )
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class Order_product_count(models.Model):
    """Количество продуктов в заказе"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE,)
    product = models.ForeignKey(Product, on_delete=models.PROTECT,)
    count = models.PositiveIntegerField()


class Payment(models.Model):
    """Модель оплаты заказа"""
    name = models.CharField(max_length=128, blank=True, default="")
    number = models.CharField(blank=False, max_length=16, default="")
    month = models.CharField(max_length=2, null=False, blank=True, default="")
    year = models.CharField(max_length=4, null=False, blank=True, default="")
    code = models.CharField(max_length=3, null=False, blank=True, default="")
    order = models.ForeignKey(Order, on_delete=models.PROTECT, null=False)
