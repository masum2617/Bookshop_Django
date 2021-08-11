from django.contrib import admin
from . models import Book
# Register your models here.

class BooksAdmin(admin.ModelAdmin):
    prepopulated_fields = { 
        'slug': ("book_title",) 
    }
admin.site.register(Book, BooksAdmin)