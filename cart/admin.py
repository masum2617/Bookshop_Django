from django.contrib import admin
from .models import Cart, Cart_Item
# Register your models here.

class Cart_ItemAdmin(admin.ModelAdmin):
    list_display = ('book', 'quantity', 'user', 'is_active', 'book_type')

admin.site.register(Cart)
admin.site.register(Cart_Item, Cart_ItemAdmin)