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
    def add(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'price': str(product.price)}
        self.session.modified = True

    def __len__(self):
        # it should also be on all pages and done by context_processors.py
        return len(self.cart)