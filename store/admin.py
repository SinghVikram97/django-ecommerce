from django.contrib import admin

from store.models import Product, Category, Order, Customer, Profile
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Profile)

# Mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile

# Extend User model
class CustomUserAdmin(admin.ModelAdmin):
    model = User
    field = ['username', 'first_name', 'last_name', 'email']
    inlines = [ProfileInline]

# Unregister the default User model way
admin.site.unregister(User)

# Register the new custom User model way
admin.site.register(User, CustomUserAdmin)