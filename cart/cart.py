from itertools import product

from store.models import Product, Profile


class Cart():
    def __init__(self, request):
        self.session = request.session
        # Get request
        self.request = request
        # If current session_key exists, get it!
        cart = self.session.get('session_key')
        
        # If user new no session_key ! Create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        # To make shopping cart work on all pages of website
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            
            # Convert python dictionary to json string
            carty = str(self.cart)
            carty = carty.replace("\'", '\"')

            # Save carty to profile model
            current_user.update(old_cart=str(carty))

    
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            
            # Convert python dictionary to json string
            carty = str(self.cart)
            carty = carty.replace("\'", '\"')

            # Save carty to profile model
            current_user.update(old_cart=str(carty))

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

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            
            # Convert python dictionary to json string
            carty = str(self.cart)
            carty = carty.replace("\'", '\"')

            # Save carty to profile model
            current_user.update(old_cart=str(carty))
        thing = self.cart
        return thing

    def delete(self, product):
        product_id = str(product)
        # Delete from dictionary
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            
            # Convert python dictionary to json string
            carty = str(self.cart)
            carty = carty.replace("\'", '\"')

            # Save carty to profile model
            current_user.update(old_cart=str(carty))

    def cart_total(self):
        # Get Product Ids
        product_ids = self.cart.keys()
        # lookup those keys in product db model
        products = Product.objects.filter(id__in=product_ids)
        # Get quantities
        quantities = self.cart

        total = 0
        for key, value in quantities.items():
            # convert key string into int to do the calculation
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total





