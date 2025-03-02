from django.urls import path
from .views import (
    SalesOrderListCreateView, SalesOrderDetailView,
    InvoiceListView,
)

urlpatterns = [
    path('sales_orders/', SalesOrderListCreateView.as_view(), name='salesorder-list-create'),
    path('sales_orders/<int:pk>/', SalesOrderDetailView.as_view(), name='salesorder-detail'),
    path('invoices/', InvoiceListView.as_view(), name='invoice-list'),
    # path('invoices/<int:pk>/', InvoiceDetailView.as_view(), name='invoice-detail'),
]
