"""
Подключение путей для приложения catalog: продукты, заказы, теги, корзина
"""
from django.urls import path
from orders.views import OrdersView, OrderDetailView, PaymentView, OrdersDetailView

app_name = 'orders'

urlpatterns = [
    path("orders", OrdersView.as_view()),
    path("order/<int:id>", OrderDetailView.as_view()),
    path("orders/<int:id>", OrdersDetailView.as_view(), name='order-detail'),
    path("payment/<int:id>", PaymentView.as_view()),
    # path("orders/<int:id>", OrderDetailView.as_view(), name='order-detail'),
    # path("payment-someone", PaymentView.as_view()), не работает/отсутствует переход на оплату и только 8 цифр,
    # в сваггере нет вообще)
    ]
