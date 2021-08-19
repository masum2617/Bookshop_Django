from books.models import Book
from django.shortcuts import render
# Create your views here.
def books(request):
    books = Book.objects.all()
    context = {
        'books':books,
    }
    return render(request, 'books/books.html', context)

def book_detail(request, category_slug, book_slug):
    single_book = Book.objects.get(category__slug = category_slug, slug= book_slug)

    context = {
        'single_book' : single_book,
    }

    return render(request, 'books/book_detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword: 
            books = Book.objects.order_by('-created_date').filter(book_title__icontains= keyword)
            books_count = books.count()
    context = {
        'books':books,
        'books_count': books_count,
    }
    return render(request, 'books/books.html', context)