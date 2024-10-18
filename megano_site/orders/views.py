from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from orders.models import Order, Order_product_count, Payment
from orders.permissions import OrderOwner
from orders.serializers import OrderSerializer, PaymentSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from cart.cart import Cart
from catalog.models import Product


class OrdersView(APIView):
    """Заказы"""
    # Доступ - прошедшим аутентификацию & владельцу заказа
    permission_classes = [IsAuthenticated & OrderOwner]

    def get(self, request: Request) -> Response:
        # Получаем в заказы отфлитрованные по пользователям объекты заказов
        orders = Order.objects.filter(user_id=request.user.pk)
        serialized = OrderSerializer(orders, many=True)
        return Response(serialized.data)

    def post(self, request: Request, *args, **kwargs) -> Response:
        data = request.data
        order_products = [
            (obj['id'], obj['count'], obj['price']) for obj in data
        ]
        products_id = [product_id[0] for product_id in order_products]
        products = Product.objects.filter(id__in=products_id)
        # В заказ помещаем созданный заказ с переменными пользователя и общей суммой заказа;
        # общую стоимость берем из класса корзины - метод total_price
        order = Order.objects.create(
            user=request.user,
            totalCost=Cart(request).total_price(),
        )
        # устанавливаем в заказ продукты
        order.products.set(products)
        # сохраняем изменения в заказе
        order.save()

        return Response({
            'orderId': order.pk
        })

class OrdersDetailView(APIView):
    permission_classes = [IsAuthenticated & OrderOwner]

    def get(self, request: Request, id):
        order = get_object_or_404(Order, pk=id)
        self.check_object_permissions(request, order)
        serializer = OrderSerializer(order)

        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderDetailView(APIView):
    """Детальная информация заказа"""
    # Доступ - прошедшим аутентификацию & владельцу заказа
    permission_classes = [IsAuthenticated & OrderOwner]

    def get(self, request: Request, id):
        order = get_object_or_404(Order, pk=id)
        self.check_object_permissions(request, order)
        serializer = OrderSerializer(order)

        cart = Cart(request).cart
        data = serializer.data
        products_in_order = data['products']

        for prod in products_in_order:
            prod['count'] = cart[str(prod['id'])]['count']

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request: Request, id) -> Response:
        """Отправка данных в заказ - по id"""
        order = Order.objects.get(pk=id)
        # проверка на доступ -пермишнс по реквесту и заказу-по id
        self.check_object_permissions(request, order)

        # кладем данные в словарь для дальнейшего заполнения таблицы Order
        data = request.data
        print('СЛОВАРЬ!', data)
        order.fullName = data['fullName']
        order.phone = data['phone']
        order.email = data['email']
        order.deliveryType = data['deliveryType']
        order.city = data['city']
        order.address = data['address']
        order.paymentType = data['paymentType']
        order.status = 'awaiting'

        # заполнение таблицы Order_product_count
        for product in data['products']:
            Order_product_count.objects.get_or_create(
                order_id=order.pk,
                product_id=product['id'],
                count=product['count'],
            )

        order.save()

        # Цифры за доставку (плюс к totalCost) поправлены в соответствии с ТЗ - в проекте стоимость указана в $
        # Проверка на тип доставки, ЕСЛИ экспресс - то с наценкой, иначе дешевле
        if data['deliveryType'] == 'express':
            order.totalCost += 5
        else:
            if order.totalCost < 23:
                order.totalCost += 2
        # Сумма корректно записывается в Базу данных "Order"
        # но на странице отображается при обычной доставке - сумма без стоимости доставки
        order.save()

        return Response(data, status=status.HTTP_200_OK)


class PaymentView(APIView):
    """Класс оплаты"""

    # Доступ - прошедшим аутентификацию & владельцу заказа
    permission_classes = [IsAuthenticated & OrderOwner]

    def post(self, request: Request, id) -> Response:
        """Пост-запрос
        :param :request - сам Request-запрос на создание платежа, id
        """

        order = Order.objects.get(id=id)
        # order = Order.objects.get(id=request.data.get('order'))
        # print('проверка, заказ = ', order)
        self.check_object_permissions(request, order)
        data = request.data
        data["order"] = id
        serializer = PaymentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        # print('проверка; сериализатор = ', serializer)

        if serializer.is_valid():
            serializer.save(order=order)
    #         # статус заказа: принят/подтвержден/в сборке/в пути/готов к выдаче/выполнен/возврат/ отмена
            order.status = 'accepted'
            order.save()
            Cart(request).clear()
    #         # Если все ок - устанавливаем статус accepted и возвращает статус 200
            return Response(status=status.HTTP_200_OK)

        # Если все не ок - возвращаем 400 ошибку
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
