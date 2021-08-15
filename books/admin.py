from django.contrib import admin
from . models import Book, Variation
# Register your models here.

class BooksAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'author', 'price', 'is_available', 'stock')
    search_fields = ('book_title', 'author')
    list_filter = ('category',)
    prepopulated_fields = { 
        'slug': ("book_title",) 
    }

class VariationAdmin(admin.ModelAdmin):
    list_display = ('book', 'variation_value1','variation_value2', 'book_type')

admin.site.register(Book, BooksAdmin)
admin.site.register(Variation, VariationAdmin)