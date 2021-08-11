from django.shortcuts import render
from books.models import Book
# Create your views here.
def home(request):
    books = Book.objects.all().filter(is_available=True)
    context = {
        'books':books,
    }
    return render(request, 'home.html', context)