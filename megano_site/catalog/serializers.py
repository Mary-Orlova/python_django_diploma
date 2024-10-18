from rest_framework import serializers
from .models import Tag, Image, Product, Category, Review, Specification, SalesProduct


class ImageSerializer(serializers.ModelSerializer):
    """Сериализатор фотографий товара"""
    class Meta:
        model = Image
        fields = ["src", "alt"]

    src = serializers.SerializerMethodField(read_only=True)

    def get_src(self, obj):
        return obj.src.url


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор подкатегории товара"""
    class Meta:
        # model = Subcategory--предыдущий вариант
        model = Category
        fields = ["id", "title", "image", "parent"]

    image = ImageSerializer()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории товара"""
    class Meta:
        model = Category
        fields = ["id", "title", "image", "subcategories"]

    image = ImageSerializer()
    subcategories = SubcategorySerializer(many=True, required=False,)


class SpecificationSerializer(serializers.ModelSerializer):
    """Сериализатор спецификации товара(характеристика и значение)"""
    class Meta:
        model = Specification
        fields = ["name", "value"]


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тэгов товара"""
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов на товар"""
    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор товаров"""
    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "fullDescription",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "specifications",
            "rating",
            "is_limited",
        ]
    images = ImageSerializer(many=True)
    tags = TagSerializer(read_only=True, many=True)
    reviews = ReviewSerializer(many=True)
    specifications = SpecificationSerializer(many=True)
    category = CategorySerializer()

    # добавляет тэг в карточку товара
    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def get_category(self, obj):
        return obj.category.title


class ProductPopularSerializer(serializers.ModelSerializer):
    """Сериализатор популярных товаров"""
    class Meta:
        model = Product
        depth = 1
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        ]

    reviews = serializers.IntegerField(source="reviews.count")
    category = serializers.IntegerField(source="category.id")


class Catalog:
    def __init__(self, items, currentPage, lastPage):
        self.items = items
        self.lastPage = lastPage
        self.currentPage = currentPage


class CatalogSerializer(serializers.Serializer):
    """Сериализатор каталога"""
    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        ]

    items = ProductSerializer(many=True)
    currentPage = serializers.IntegerField()
    lastPage = serializers.IntegerField()

    images = ImageSerializer(many=True, required=True)
    tags = TagSerializer(many=True, required=False)
    count = serializers.SerializerMethodField(method_name="get_count")
    price = serializers.SerializerMethodField(method_name="get_price")
    freeDelivery = serializers.SerializerMethodField(method_name="get_freeDelivery")
    date = serializers.SerializerMethodField(method_name="date_to_string")
    reviews = serializers.SerializerMethodField(method_name="get_reviews")


class SalesProductSerializer(serializers.ModelSerializer):
    """Сериализатор скидок/акций товаров"""
    class Meta:
        model = SalesProduct
        fields = ["id", "price", "salePrice", "dateFrom", "dateTo", "title", "images"]

    price = serializers.FloatField(source="product.price")
    title = serializers.CharField(source="product.title")
    images = ImageSerializer(source="product.images", many=True)
