from books.models import Book  
from cart.models import Cart_Item
from .models import Order, OrderProduct
from .forms import OrderForm
from django.shortcuts import redirect, render
import datetime
# Create your views here.

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def place_order(request): 
   current_user = request.user
   total = 0
   cart_items = Cart_Item.objects.filter(user=current_user)

   for item in cart_items:
       total += (item.book.price * item.quantity)


   if request.method == "POST":
       form = OrderForm(request.POST)
       if form.is_valid():
           data = Order()
           data.user = current_user
           data.first_name = form.cleaned_data['first_name']
           data.last_name = form.cleaned_data['last_name']
           data.phone = form.cleaned_data['phone']
           data.email = form.cleaned_data['email']
           data.address_line_1 = form.cleaned_data['address_line_1']
           data.address_line_2 = form.cleaned_data['address_line_2']
           data.country = form.cleaned_data['country']
           data.city = form.cleaned_data['city']
           data.order_note = form.cleaned_data['order_note']
           data.last_name = form.cleaned_data['last_name']
           data.phone = form.cleaned_data['phone']
           data.email = form.cleaned_data['email']
           data.address_line_1 = form.cleaned_data['address_line_1']
           data.address_line_2 = form.cleaned_data['address_line_2']
           data.country = form.cleaned_data['country']
           data.city = form.cleaned_data['city']
           data.order_note = form.cleaned_data['order_note']
           data.ip = get_client_ip(request)
           data.order_total = total
           data.delivery_charge = 50

           data.save()       

           yr = int(datetime.date.today().strftime('%Y'))
           dt = int(datetime.date.today().strftime('%d'))
           mt = int(datetime.date.today().strftime('%m'))
           d = datetime.date(yr,mt,dt)
           current_date = d.strftime("%Y%m%d") 
           order_number = current_date + str(data.id) 
           data.order_number = order_number
           data.is_ordered = True
           data.save()

           order = Order.objects.get(user=current_user, is_ordered=True)
           
           for item in cart_items:
               ordered_product = OrderProduct()

               ordered_product.order_id = order.id
               ordered_product.user_id = current_user.id
               ordered_product.product_id = item.book_id
               ordered_product.product_price = item.book.price
               ordered_product.ordered = True
               ordered_product.quantity = item.quantity
               ordered_product.save()

                # reduce stock 
               book = Book.objects.get(id=item.book_id)
               book.stock -= item.quantity
               book.save()

       
        
        #    order.is_ordered = True            

           return redirect('order_complete')
   else:
        return redirect('checkout')
 

def order_complete(request):
    current_user = request.user
    order = Order.objects.all().filter(user=current_user)
    orderedProduct = OrderProduct.objects.all().filter(user=current_user)

    context = {
        'order':order,
        'orderedProduct': orderedProduct,
    }

    return render(request, 'orders/order_complete.html',context)



