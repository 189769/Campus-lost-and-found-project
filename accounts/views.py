from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required

# Registration view
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # creates user and profile
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
        else:
            print(form.errors)  # debug form errors
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # change 'home' to your dashboard
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')
