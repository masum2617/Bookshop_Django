from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.books, name='books'),
    # path('detail/', views.book_detail, name='book_detail'),
    path('category/<slug:category_slug>', views.books, name='category'),
    path('category/<slug:category_slug>/<slug:book_slug>', views.book_detail, name='book_detail'),
    path('search/', views.search, name='search'),
    path('submit_review/<int:book_id>/', views.submit_review, name='submit_review')
]