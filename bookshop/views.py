from django.shortcuts import get_object_or_404, render
from books.models import Book,Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# Create your views here.
def home(request,category_slug=None):
    # books = Book.objects.all().filter(is_available=True)

    if category_slug is not None:
        book_category = get_object_or_404(Category, slug=category_slug)
        books = Book.objects.filter(category=book_category, is_available=True)
        paginator = Paginator(books, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
      
    else:
        books = Book.objects.all().filter(is_available=True)
        paginator = Paginator(books, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        


    context = {
        'books':paged_products,
    }
    return render(request, 'home.html', context)


