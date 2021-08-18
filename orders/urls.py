from django.urls import path
from .import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    # path('detail/', views.book_detail, name='book_detail'),

]