from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.http import request
from .models import Account
from orders.models import Order
from django.shortcuts import redirect, render
from .forms import RegistrationForm
from django.contrib.auth import authenticate
from cart.models import Cart, Cart_Item
from cart.views import _cart_id
from django.http import HttpResponse
# Create your views here.
def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # repeate_password = form.cleaned_data['repeat_password']
            city = form.cleaned_data['city']
            phone_number = form.cleaned_data['phone_number']
            username = first_name + phone_number[-3:]

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.city = city
            user.phone_number = phone_number
            user.is_active = True
            user.save()


                        
            # registration verify with activation link
            # current_site = get_current_site(request)
            # mail_subject = "Please confirm your registration process"
            # message = render_to_string('users/user_verification.html', {
            #     'user':user,
            #     'domain':  current_site,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': default_token_generator.make_token(user), 
            # })
            # to_mail = email
            # send_mail = EmailMessage(mail_subject, message,to=[to_mail])
            # send_mail.send()
            
            # messages.success(request, "Check Email to Verify Your Account!")
            messages.success(request, "You are successfully registered! You can now login")
            return redirect('login')

    else:
        form = RegistrationForm(request.POST)    

    context = {
        'form':form
    }
    return render(request, 'users/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = Cart_Item.objects.filter(cart_item=cart).exists()
                if is_cart_item_exists:
                    cart_items = Cart_Item.objects.filter(cart_item=cart)
                    for item in cart_items:
                        item.user = user
                        item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request,'Login Successful')
            
            # redirect user to next direction from checkout
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('home')
        else:
            messages.error(request, "Email or Passwrod is incorrect"
            )
            return redirect('login')
    return render(request, 'users/login.html')
    
def logout(request):
    auth.logout(request)
    # messages.success(request, "You are now Logged Out!")
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations! Your account is Verified!")
        return redirect('login')
    else:
        messages.error(request, "Verification Failed!")
        return redirect('register')


def forgotpassword(request):
    if request.method == "POST":
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__iexact=email)
            # forgot password 
            current_site = get_current_site(request)
            mail_subject = "Reset Password"
            message = render_to_string('users/reset_password.html', {
                'user':user,
                'domain':  current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user), 
            })
            to_mail = email
            send_mail = EmailMessage(mail_subject, message,to=[to_mail])
            send_mail.send()

            messages.success(request, "Check your Email to reset your password")
            return redirect('login')
        else:
            messages.error(request, "Account Does not exist")
            return redirect('forgotpassword')
    return render(request, 'users/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, "Reset your Password")
        return redirect('resetPassword')
    else:
        messages.error(request,"Link Expired!")
        return redirect('login')


def resetPassword(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Reset password Successful!')
            return redirect('login')
        else:
            messages.error(request, "Password do not match!")
            return redirect('resetPassword')
    else:
        return render(request, 'users/resetPassword.html')

def dashboard(request):
    current_user = request.user

    orders = Order.objects.order_by('-created_at').filter(user_id=current_user.id, is_ordered=True)
    total_order = orders.count()

    context ={
        'total_order':total_order,
    }

    return render(request, 'users/dashboard.html', context)

def myorders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders':orders,
    }
    return render(request, 'users/myorders.html', context)