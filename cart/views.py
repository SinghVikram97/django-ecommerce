from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    return render(request, "cart_summary.html", {"cart_products":cart_products})
def cart_add(request):
    # get the cart
    cart = Cart(request)
    # test for POST
    if request.POST.get('action') == 'post':
        # get stuff
        product_id = int(request.POST.get('product_id'))
        # lookup product in the database
        product = get_object_or_404(Product, id=product_id)
        # Save to session
        cart.add(product=product)
        # Return Response
        # response = JsonResponse({'Product Name: ': product.name})
        # Instead lets get Cart Quantity
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        return response

def cart_delete(request):
    pass
def cart_update(request):
    pass

