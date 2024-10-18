"""
Настройки панели администратора(управление):
 товарами, категории товаров, заказами, отзывами
"""
from django.contrib import admin
from .models import Category, Product, Image, Tag, Review


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Tag)
admin.site.register(Review)