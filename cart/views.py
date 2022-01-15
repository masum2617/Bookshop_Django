from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from cart.models import Cart_Item
from cart.models import Cart
from django.shortcuts import redirect, render
from books.models import Book, Variation
# Create your views here.
from django.db.models import Q

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def cart(request):
    try:
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
    except ObjectDoesNotExist:
        pass

    context = {
        'cart_items': cart_items,
        'total_price':total_price,
    }
    return render(request, 'books/cart.html', context)

def add_to_cart(request, book_id):
    value = ''
    current_user = request.user
    single_book = Book.objects.get(id=book_id)
    # if request.method == 'POST':
    #     value = request.POST['cover']
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
            # cart_item.book_type = value
            cart_item.save()
        except Cart_Item.DoesNotExist:
            cart_item = Cart_Item.objects.create(
                book =single_book,
                quantity = 1,
                cart_item = cart,
                # book_type = value,
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
            # return redirect('cart')
        cart.save()
        try: 
            cart_item = Cart_Item.objects.get(book=single_book, cart_item=cart)
            
            if request.method =='POST':
                cart_item.book_type = value
            cart_item.quantity +=1
           
            cart_item.save()
        except Cart_Item.DoesNotExist:
            cart_item = Cart_Item.objects.create(
                book = single_book,
                cart_item = cart,
                quantity = 1,
                book_type = value
                
            
            )
            cart_item.save()  
        return redirect('cart')
    # context = {
    #     'single_book':single_book,
    # }
    # return render(request, 'books/cart.html', context)

def remove_cart(request, book_id, cart_item_id):
    single_book = Book.objects.get(id=book_id)
    if request.user.is_authenticated:
        # cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = Cart_Item.objects.get(book=single_book, user=request.user,id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = Cart_Item.objects.get(book=single_book, cart_item=cart,id=cart_item_id)
    if cart_item.quantity >1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_item(request, book_id,cart_item_id):
    single_book = Book.objects.get(id=book_id)
    if request.user.is_authenticated:
        cart_item = Cart_Item.objects.get(book=single_book, user=request.user,id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = Cart_Item.objects.get(book=single_book, cart_item=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

@login_required(login_url='login')
def checkout(request):
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
    return render(request, 'books/checkout.html', context)