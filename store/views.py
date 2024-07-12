from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def about(request):
    return render(request, 'about.html', {})


def product(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product.html', {'product': product})


def category(request, categoryselected):
    try:
        category = Category.objects.get(name=categoryselected)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {"products": products, "category": category})
    except:
        messages.success(request, "Category does not exist")
        return redirect('home')


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()
            login(request, current_user)
            messages.success(request, 'User Info Has Been Updated!!')
            return redirect('home')
        return render(request, 'update_info.html', {'form': form})
    else:
        messages.success(request, 'Please login to update your profile')
        return redirect('home')

    
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(user=current_user, data=request.POST)

            # is the form valid
            if form.is_valid():
                form.save()
                messages.success(request, 'Password has been updated')
                login(request, current_user)
                return redirect('home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
                   
        else:
            form = ChangePasswordForm(user=current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.success(request, 'Please login to update your password')
        return redirect('home')
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, 'User Has Been Updated!!')
            return redirect('home')
        return render(request, 'update_user.html', {'user_form': user_form})
    else:
        messages.success(request, 'Please login to update your profile')
        return redirect('home')
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have registered successfully. Please fill out the form below to complete your profile.')
            return redirect('update_info')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})
