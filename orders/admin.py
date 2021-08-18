from .models import Order, OrderProduct, Payment
from django.contrib import admin


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'phone', 'city' ,'status', 'is_ordered', 'created_at')

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'ordered', 'quantity' ,'created_at')


# Register your models here.
admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)