from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Product, Category, Tag
from .serializers import ProductSerializer, CategorySerializer, TagSerializer
from django.core.cache import cache
from users.permissions import IsAdmin, IsSalesRep, IsTraderOrCustomerReadOnly, IsTrader, IsOwner

# from ..users.permissions import IsAdmin, IsSalesRep, IsTraderOrCustomerReadOnly


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdmin()]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdmin()]


class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [IsAuthenticated, IsTrader]

# class OrderListCreateView(generics.ListCreateAPIView):
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated, IsTrader]
#
#     def get_queryset(self):
#         return Order.objects.filter(trader=self.request.user)
#


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [IsAuthenticated, IsAdmin | IsSalesRep | IsTraderOrCustomerReadOnly]
    @property
    def permission_classes(self):
        if self.request.method == 'GET':
            return [AllowAny]
        return [IsTrader | IsSalesRep | IsAdmin]

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [IsAuthenticated, IsAdmin | IsSalesRep | IsTraderOrCustomerReadOnly]
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsOwner()]


class MyProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)