from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.timezone import now
from .models import Order, Transaction
from .serializers import OrderSerializer, TransactionSerializer
from users.permissions import IsTrader, IsAdmin, IsOwner


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def permission_classes(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny]
        return [IsTrader]


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [IsOwner()]

class ExecuteOrderView(APIView):
    permission_classes = [IsOwner]

    def post(self, request, pk):
        try:
            order = Order.objects.get(id=pk, user=request.user, status='pending')
            executed_price = order.price
            transaction = Transaction.objects.create(order=order, executed_price=executed_price, executed_at=now(), user=request.user)

            order.status = 'completed'
            order.save()

            return Response({"message": "Order executed", "transaction": TransactionSerializer(transaction).data})
        except Order.DoesNotExist:
            return Response({"error": "Order not found or already completed"}, status=400)



class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        queryset = Transaction.objects.filter(order__user=self.request.user)
        product_id = self.request.query_params.get('product')
        date = self.request.query_params.get('date')

        if product_id:
            queryset = queryset.filter(order__product_id=product_id)
        if date:
            queryset = queryset.filter(executed_at__date=date)

        return queryset


class TransactionDetailView(generics.RetrieveAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Transaction.objects.filter(order__user=self.request.user)

class MyOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

