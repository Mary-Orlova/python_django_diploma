"""
В этом модуле лежат различные представления.

Разные view для интернет-магазина: по товарам, заказам и тд.
"""
import datetime
from django.db.models import Count
from django.http import JsonResponse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Tag, Product, Category, SalesProduct
from .serializers import (
    ProductSerializer,
    ReviewSerializer,
    CategorySerializer,
    SalesProductSerializer,
    TagSerializer,
)


class TagsView(APIView):
    """Тэги-отображение на странице каталога в Популярных тегах"""
    def get(self, request: Request) -> Response:
        tags = Tag.objects.all()
        serialized = TagSerializer(
            tags,
            many=True,
        )
        return Response(serialized.data)


class ProductView(APIView):
    """Товары"""
    def get(self, request: Request, **kwargs) -> Response:
        product = Product.objects.get(id=self.kwargs.get("id"))
        serializer = ProductSerializer(product, read_only=True)
        return Response(serializer.data)


class ProductDetailAPIView(APIView):
    """Детальное представление товара-карточка товара"""
    def get(self, request, *args, **kwargs) -> Response:
        id = kwargs.get("id")
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class PopularProductsView(APIView):
    """Представление популярных товаров"""

    def get(self, request) -> Response:
        products = Product.objects.order_by("rating")[:8]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SalesView(APIView):
    """Представление акционных товаров"""
    def get(self, request: Request) -> Response:
        sales = SalesProduct.objects.all()
        serializer = SalesProductSerializer(
            sales,
            many=True,
        )
        data = {
            "items": serializer.data,
            "currentPage": int(request.GET.get("currentPage")),
            "lastPage": 2,
        }
        return Response(data, status=status.HTTP_200_OK)


class LimitedProductsView(APIView):
    """Представление товаров ограниченного тиража"""
    def get(self, request) -> Response:
        products = Product.objects.filter(is_limited=True)[:16]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductReviewView(APIView):
    """Отзывы на товары"""
    def post(self, request: Request, id) -> Response:
        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            review = serializer.save()
            product = Product.objects.get(id=id)
            product.reviews.add(review)
            reviews = product.reviews.all().values()
            return JsonResponse(list(reviews), safe=False)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BannersView(APIView):
    """Баннеры"""
    def get(self, request) -> Response:
        products = Product.objects.filter(banner=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoriesView(APIView):
    """Категории товаров"""
    def get(self, request: Request) -> Response:
        # categories = Category.objects.all()
        categories = Category.objects.filter(parent=None)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CatalogView(APIView):
    """Каталог товаров"""
    def get(self, request: Request) -> Response:
        """Метод получения параметров фильтрации и представления каталога товаров"""
        name = request.query_params.get('filter[name]') or None
        # если товар доступен
        if request.query_params.get('filter[available]') == 'true':
            archived = False
        else:
            archived = True
        # если бесплатная доставка
        if request.query_params.get('filter[freeDelivery]') == 'true':
            freeDelivery = True
        else:
            freeDelivery = False
        # записываем в переменную теги
        tags = request.query_params.getlist('tags[]') or None
        # tags = Tag.objects.filter(id__in=map(int, dict(request.GET).get("tags[]", [])))--название тега, а выше id

        # записываем в переменную минимальную стоимость
        minPrice = request.query_params.get('filter[minPrice]')
        # записываем в переменную максимальную стоимость
        maxPrice = request.query_params.get('filter[maxPrice]')
        # записываем в переменную категории товаров
        category = request.META['HTTP_REFERER'].split('/')[4] or None
        # записываем в переменную сортировку
        sort = request.GET.get('sort')
        if request.GET.get('sortType') == 'inc':
            sortType = '-'
        else:
            sortType = ''
        # записываем в переменную параметры сортивровки товаров по цене
        products_list = Product.objects.filter(
            price__range=(minPrice, maxPrice),
            count__gt=0,
        )
        # проверка на категорию/начало фильрации по ней
        if category:
            if category.startswith('?filter='):
                if name is None:
                    name = category[8:]
            else:
                parent_categories = Category.objects.filter(
                    parent_id=category,
                )
                all_categories = [subcategory.pk for subcategory in parent_categories]
                all_categories.append(int(category))
                products_list = products_list.filter(
                    category_id__in=all_categories,
                )
        if name:
            products_list = products_list.filter(
                title__iregex=name,
            )
        if tags:
            products_list = products_list.filter(
                tags__in=tags,
            )
        if freeDelivery:
            products_list = products_list.filter(
                freeDelivery=freeDelivery,
            )
        # если архивированные/недоступные товары
        if archived:
            products_list = products_list.filter(
                archived=archived,
            )
        # если сортировка по отзывам
        if sort == 'reviews':
            products_list = products_list.annotate(
                count_reviews=Count('reviews'),
            ).order_by(
                f'{sortType}count_reviews'
            )
        else:
            products_list = products_list.order_by(
                f'{sortType}{sort}',
            )
        products_list = products_list.prefetch_related(
            'images',
            'tags',
        )
        serialized = ProductSerializer(
            products_list,
            many=True,
        )
        currentPage = int(request.GET.get("currentPage"))
        data = {"items": serialized.data, "currentPage": currentPage, "lastPage": 2}
        return Response(data, status=status.HTTP_200_OK)
