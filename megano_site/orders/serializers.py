import random

from rest_framework import serializers
from catalog.serializers import ProductSerializer
from orders.models import Order, Payment


def validate_payment(number) -> str:
    """Проверка валидности кол-ва цифр номера карты
    :param number: номер карты
    """
    # проверка работает, но ошибку не пишет пользователю-только в логах

    # print('количество цифр номера карты=', len(number))
    # print('номер карты',number)

    if len(number) != 16:
        raise serializers.ValidationError("Номер карты должен состоять из 16 цифр.")
    if int(number) % 2 != 0 or int(number[-2:-1]) == 0:
        raise serializers.ValidationError("Номер карты не может быть нечетный и/или оканчиваться на 0")
    return number


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'createdAt',
            'fullName',
            'email',
            'phone',
            'deliveryType',
            'paymentType',
            'totalCost',
            'status',
            'city',
            'address',
            'products',
        )

    products = ProductSerializer(
        many=True,
        required=True,
    )
    fullName = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()

    def get_fullName(self, instance):
        return instance.user.profile.fullName

    def get_email(self, instance):
        return instance.user.profile.email

    def get_phone(self, instance):
        return instance.user.profile.phone


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор оплаты заказа"""
    class Meta:
        model = Payment
        fields = '__all__'
        # fields = 'name', 'number', 'month', 'year', 'code'
        extra_kwargs = {
            'number': {'validators': [validate_payment]},
        }
