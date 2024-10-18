from decimal import Decimal
from rest_framework import serializers
from catalog.models import Product
from catalog.serializers import ImageSerializer


class BasketSerializer(serializers.ModelSerializer):
    """Сериализатор корзины"""
    class Meta:
        model = Product
        fields = '__all__'

    count = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    # подключение отображения изображдений товаров в корзине
    images = ImageSerializer(many=True)

    # ссылка - переход в картоку товара в корзине
    href = serializers.StringRelatedField()

    def get_count(self, obj):
        return self.context.get(str(obj.pk)).get('count')

    def get_price(self, obj):
        return Decimal(self.context.get(str(obj.pk)).get('price'))
