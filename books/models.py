from category.models import Category
from django.db import models
from datetime import datetime
from django.urls import reverse
# Create your models here.

class Book(models.Model):
    book_title  = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    slug        = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=500, blank=True)
    price       = models.IntegerField()
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    photo_main  = models.ImageField(upload_to='photos/books/%Y/%m/%d/')
    photo_1     = models.ImageField(upload_to='photos/books/%Y/%m/%d/', blank=True)
    photo_2     = models.ImageField(upload_to='photos/books/%Y/%m/%d/', blank=True)
    photo_3     = models.ImageField(upload_to='photos/books/%Y/%m/%d/', blank=True)
    created_date = models.DateTimeField(default=datetime.now, blank=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book_title
    
    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'category_slug' : self.category.slug, 'book_slug':self.slug })



