from category.models import Category
from books.models import Book
from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.
def books(request,category_slug=None):

    if category_slug is not None:
        book_category = get_object_or_404(Category, slug=category_slug)
        books = Book.objects.filter(category=book_category, is_available=True)
        paginator = Paginator(books, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        books_count = books.count()
    else:
        books = Book.objects.all().filter(is_available=True)
        paginator = Paginator(books, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        books_count = books.count()


    context = {
        'books':paged_products,
        'books_count':books_count,
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