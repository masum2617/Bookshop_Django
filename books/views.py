from books.models import Book
from django.shortcuts import render
# Create your views here.
def books(request):
    return render(request, 'books/books.html')

def book_detail(request, category_slug, book_slug):
    single_book = Book.objects.get(category__slug = category_slug, slug= book_slug)

    context = {
        'single_book' : single_book,
    }

    return render(request, 'books/book_detail.html', context)