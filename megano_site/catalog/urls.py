"""
Подключение путей для приложения catalog: продукты, заказы, теги, корзина
"""
from django.urls import path
from .views import (
    TagsView,
    CategoriesView,
    CatalogView,
    ProductDetailAPIView,
    ProductReviewView,
    PopularProductsView,
    LimitedProductsView,
    SalesView,
    BannersView,
)


app_name = 'catalog'


urlpatterns = [
    path('tags/', TagsView.as_view(), name='tags_list'),
    path('catalog/', CatalogView.as_view(), name="catalog_list"),
    path('categories/', CategoriesView.as_view(), name='categories_list'),
    path('product/<int:id>', ProductDetailAPIView.as_view()),
    path('product/<int:id>/reviews', ProductReviewView.as_view()),
    path('products/popular/', PopularProductsView.as_view(), name='popular_products'),
    path('products/limited/', LimitedProductsView.as_view(), name='limited_products'),
    path('sales/', SalesView.as_view(), name='sales_list'),
    path('banners/', BannersView.as_view(), name='banners_list'),
]
