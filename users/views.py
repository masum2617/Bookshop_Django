from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from .models import Account
from django.shortcuts import redirect, render
from .forms import RegistrationForm
from django.contrib.auth import authenticate
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
            
            user.save()
            messages.success(request, "Successfully Registered")
            return redirect('register')
            # if password == repeate_password:
            #     if Account.objects.filter(email=email).exists():
            #         messages.error(request, "Email Already Exists!")
            #         return redirect('register')
            #     else:
            #         user.save()
            #         messages.success(request, "Registraion successful!")
            #         return redirect('home')

            # else:
            #     messages.error(request, "Password do not Match!")
            #     return redirect('register')
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
            auth.login(request, user)
            messages.success(request,'Login Successful')
            return redirect('home')
        else:
            messages.error(request, "Email or Passwrod is incorrect"
            )
            return redirect('login')
    return render(request, 'users/login.html')
    
def logout(request):
    auth.logout(request)
    messages.success(request, "You are now Logged Out!")
    return redirect('login')
    