from django.contrib import admin

# Register your models here.
from .models import Order, Transaction

admin.site.register(Order)
admin.site.register(Transaction)