from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact

# Create your views here.

def register(request):
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passwords match
        if password == password2:
           # Check if username is already in database
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect('register')
            else: 
                # Check if email address is already in database
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email address is taken')
                    return redirect('register')
                else: 
                    # can register this user!
                    user = User.objects.create_user(username=username, password=password, 
                    email=email, first_name=first_name, last_name=last_name)
                    # Login after register
                    # auth.login(request, user)
                    # messages.success(request, 'You are now logged in!')
                    # return redirect('index')

                    user.save()
                    messages.success(request, 'You are now registered. Please login')
                    return redirect('login')
        else: 
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else: 
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        # get 'username' and 'password' input value from form
        username = request.POST['username']
        password = request.POST['password']
        # 1 authenticate user using authenticate() method.
        user = auth.authenticate(username=username, password=password)
        # check if user exists in database
        if user is not None:
            # 2 log-in a user. so authenticate first to check if user credential is valid. 
            # if so, login a user -- IMPORTANT ---
            auth.login(request, user)
            return redirect('dashboard')
        else: 
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    # logout is a function that is registered as url
    if request.method == 'POST':
        # just call auth.logout function here.... pass in data from request.
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')

def dashboard(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to acceess the page')
        return redirect('login')
    else:
        user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
        contexts = {
            'contacts': user_contacts
        }
        return render(request, 'accounts/dashboard.html', contexts)