from django.shortcuts import render, redirect
from .models import Product, Category, Profile, UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart

def home(request):
    products = Product.objects.all()
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = UserProfile.objects.create(user=request.user)
    return render(request, 'home.html', {'products': products, 'user_profile': user_profile})


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

def search(request):
    # Determine if the search form has been submitted
    if request.method == 'POST':
        searched = request.POST['searched']
        
        # Query The products DB model
        search_results = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

        # Test for Null
        if not search_results:
            messages.success(request, "No search results found")
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched': search_results})
    else:
        return render(request, 'search.html', {})
def update_info(request):
    if request.user.is_authenticated:
        # Get the current user
        current_user = Profile.objects.get(user__id=request.user.id)
        
        # Get the current user shipping info
        try:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        except ShippingAddress.DoesNotExist:
            shipping_user = None

        # Get original user form
        form = UserInfoForm(request.POST or None, instance=current_user)
        
        # Get user's Shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            login(request, current_user)
            messages.success(request, 'User Info Has Been Updated!!')
            return redirect('home')
        return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})
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

            # Do some shopping cart stuff here
            current_user = Profile.objects.get(user__id=request.user.id)
            # Get their saved cart from database
            saved_cart = current_user.old_cart
            # Convert json string to python dictionary
            if saved_cart:
                converted_cart = json.loads(saved_cart)
                # Add the loaded cart to the session
                
                # get the cart
                cart = Cart(request)
                # Loop through the cart and add each item to the session
                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)

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
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user_profile = UserProfile.objects.get(user=user)
            user_profile.profile_picture = form.cleaned_data.get('profile_picture')
            user_profile.save()
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
def edit_profile_picture(request):
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.profile_picture = request.FILES['profile_picture']
        user_profile.save()
        messages.success(request, 'Your profile picture has been updated.')
        return redirect('home')
    else:
        return render(request, 'edit_profile_picture.html', {})