from datetime import datetime
from django.db import models
from books.models import Book
from users.models import Account
# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.cart_id

class Cart_Item(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    cart_item = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.book.book_title

    def item_total(self):
        return self.quantity * self.book.price
