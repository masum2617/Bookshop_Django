from django.urls import path
from .import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_cart/<int:book_id>/', views.remove_cart, name='remove_cart'),
    path('remove_item/<int:book_id>/', views.remove_item, name='remove_item'),

]