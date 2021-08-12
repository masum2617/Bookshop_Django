from django.contrib import admin
from . models import Book
# Register your models here.

class BooksAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'author', 'price', 'is_available', 'stock')
    search_fields = ('book_title', 'author')
    list_filter = ('category',)
    prepopulated_fields = { 
        'slug': ("book_title",) 
    }
admin.site.register(Book, BooksAdmin)