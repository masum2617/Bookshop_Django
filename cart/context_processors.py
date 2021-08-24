from .models import Cart, Cart_Item
from .views import _cart_id

def itemCounter(request):
    item_counter = 0
    if 'admin' in request.path:
        return {}
    try:
        if request.user.is_authenticated:
            cart_items = Cart_Item.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            cart_items = Cart_Item.objects.all().filter(cart_item=cart[:1]) 
        for item in cart_items:
            item_counter += item.quantity
    except Cart.DoesNotExist:
        item_counter = 0
    # print(dict(item_counter=item_counter))
    return dict(item_counter = item_counter)