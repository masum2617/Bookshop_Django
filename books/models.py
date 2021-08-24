from category.models import Category
from django.db import models
from datetime import datetime
from django.urls import reverse
from users.models import Account
# Create your models here.

class Book(models.Model):

    book_title  = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    slug        = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=1000, blank=True)
    price       = models.IntegerField()
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    photo_main  = models.ImageField(default='default.jpg' ,upload_to='photos/books/%Y/%m/%d/')
    photo_1     = models.ImageField(upload_to='photos/books/%Y/%m/%d/', blank=True)
    photo_2     = models.ImageField(upload_to='photos/books/%Y/%m/%d/', blank=True)
    photo_3     = models.ImageField(upload_to='photos/books/%Y/%m/%d/', blank=True)
    created_date = models.DateTimeField(default=datetime.now, blank=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book_title
    
    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'category_slug' : self.category.slug, 'book_slug':self.slug })


BOOK_TYPE = (
    ('cover', 'cover'),
)

class Variation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_type = models.CharField(max_length=30, choices=BOOK_TYPE, null=True)
    variation_value1 = models.CharField(max_length=100)
    variation_value2 = models.CharField(max_length=100, blank=True)
    created_date = models.DateTimeField(default=datetime.now, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.variation_value1+self.variation_value2

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at =  models.DateTimeField(default=datetime.now, blank=True)
    updated_at =  models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.subject    




