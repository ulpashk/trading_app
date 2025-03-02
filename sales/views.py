from rest_framework import generics, permissions
from users.permissions import IsAdmin, IsTrader, IsOwner
from .models import SalesOrder, Invoice
from .serializers import SalesOrderSerializer, InvoiceSerializer
from django.shortcuts import get_object_or_404


class SalesOrderListCreateView(generics.ListCreateAPIView):
    serializer_class = SalesOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SalesOrder.objects.filter(customer=self.request.user)


class SalesOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SalesOrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return SalesOrder.objects.filter(customer=self.request.user)


class InvoiceListView(generics.ListAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects.filter(sales_order__customer=self.request.user)
