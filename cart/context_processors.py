from .cart import Cart
# Let's create context processor so our cart can work on all pages of the website
def cart(request):
    # Return default data from our Cart
    return {'cart': Cart(request)}
