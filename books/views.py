from django.contrib import messages
from category.models import Category
from books.models import Book, Review
from .forms import ReviewForm
from orders.views import get_client_ip
from django.shortcuts import get_object_or_404, redirect, render
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


    # getting all user reviews
    reviews = Review.objects.filter(book_id=single_book.id, status=True)
    context = {
        'single_book' : single_book,
        'reviews':reviews,
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

def submit_review(request, book_id):
    url = request.META.get('HTTP_REFERER') #store previous url
    if request.method == "POST":
        try:
            review = Review.objects.get(user__id=request.user.id, book__id=book_id)
            form = ReviewForm(request.POST,instance=review)
            form.save()
            messages.success(request, "Review updated")
            return redirect(url)
        except Review.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = Review()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.ip = get_client_ip(request)
                data.book_id = book_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Review successfully submited")
                return redirect(url)