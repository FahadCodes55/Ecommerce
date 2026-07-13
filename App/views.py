from django.contrib import auth, messages
from django.shortcuts import render, redirect
from .models import Item, User, ContactUs

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, f"Login successful! {user.username}" )
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    else:
        return render(request, 'App/Authentication/login.html')

def logout(request):
        auth.logout(request)
        messages.info(request, "You have logged out successfully.")
        return redirect('/')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')

        else:
            messages.info(request, "Password Doesn't match")
            return redirect('register')

    else:
        return render(request, 'App/Authentication/register.html')

def success(request):
    return redirect('/')


def home(request):
    query = Item.objects.order_by()
    # If you have used for specific price , date use order_by('-field_name')[:2]
    return render(request, 'App/KidStore.html', {'items' : query})


def shop(request):
    query = Item.objects.all()
    return render(request, 'App/shop.html', {'items' : query})

def contact_form(request):
    if request.method == 'POST':
        user_name = request.POST.get('name')
        user_email = request.POST.get('email')
        user_subject = request.POST.get('subject')
        user_message = request.POST.get('message')

        ContactUs.objects.create(
            name=user_name,
            email=user_email,
            subject=user_subject,
            message=user_message
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect('home')

    return render(request, 'App/KidStore.html')