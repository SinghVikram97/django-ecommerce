from store.models import Product


class Cart():
    def __init__(self, request):
        self.session = request.session
        # If current session_key exists, get it!
        cart = self.session.get('session_key')
        # If user new no session_key ! Create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        # To make shopping cart work on all pages of website
        self.cart = cart
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

    def __len__(self):
        # it should also be on all pages and done by context_processors.py
        return len(self.cart)
    def get_prods(self):
        # Get ids from cart
        product_ids = self.cart.keys()
        # Use ids to lookup products in db model
        products = Product.objects.filter(id__in=product_ids)
        # Return those looked up products
        return products
    def get_quants(self):
        quantities = self.cart
        return quantities
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # Get cart
        ourcart = self.cart
        # Update Dictionary/cart
        ourcart[product_id] = product_qty

        self.session.modified = True

        thing = self.cart
        return thing
