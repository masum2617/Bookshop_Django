from cart.models import Cart_Item
from cart.models import Cart
from django.shortcuts import redirect, render
from books.models import Book
# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def cart(request):
    total_price =0
    cart_items = None
    current_user = request.user
    if current_user.is_authenticated:
        cart_items = Cart_Item.objects.filter(user=current_user, is_active=True)
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = Cart_Item.objects.filter(cart_item=cart)

    for item in cart_items:
        total_price += item.book.price * item.quantity 


    
    context = {
        'cart_items': cart_items,
        'total_price':total_price,
    }
    return render(request, 'books/cart.html', context)

def add_to_cart(request, book_id):
    current_user = request.user
    single_book = Book.objects.get(id=book_id)
    if current_user.is_authenticated:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _cart_id(request))
        
        cart.save()

        try:
            cart_item = Cart_Item.objects.get(book=single_book, cart_item= cart)
            cart_item.quantity +=1
            cart_item.user = current_user
            cart_item.save()
        except Cart_Item.DoesNotExist:
            cart_item = Cart_Item.objects.create(
                book =single_book,
                quantity = 1,
                cart_item = cart,
                user = current_user

            )
            cart_item.save()
        return redirect('cart')
    # if user not logged in
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _cart_id(request))
        cart.save()
        try: 
            cart_item = Cart_Item.objects.get(book=single_book, cart_item=cart)
            cart_item.quantity +=1
            cart_item.save()
        except Cart_Item.DoesNotExist:
            cart_item = Cart_Item.objects.create(
                book = single_book,
                cart_item = cart,
                quantity = 1,
            
            )
            cart_item.save()  
        return redirect('cart')
    # context = {
    #     'single_book':single_book,
    # }
    # return render(request, 'books/cart.html', context)

def remove_cart(request, book_id):
    single_book = Book.objects.get(id=book_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = Cart_Item.objects.get(book=single_book, cart_item=cart)
    if cart_item.quantity >1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_item(request, book_id):
    single_book = Book.objects.get(id=book_id)

    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = Cart_Item.objects.get(book=single_book, cart_item=cart)
    cart_item.delete()
    return redirect('cart')

