from rest_framework import serializers
from .models import SalesOrder, Invoice

class SalesOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrder
        fields = ['id', 'customer', 'product', 'quantity', 'price', 'status', 'created_at']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

class InvoiceSerializer(serializers.ModelSerializer):
    sales_order = SalesOrderSerializer(read_only=True)

    class Meta:
        model = Invoice
        fields = ['id', 'sales_order', 'pdf', 'created_at']
