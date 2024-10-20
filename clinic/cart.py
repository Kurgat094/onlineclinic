class Cart():
    def _init_ (self.request):
        self.session=request.session
        cart=self.session.get('session_key')
        # if user is new ,no session key create
        if 'session_key' not in request.session:
            cart=self.session.get('session_key')
            
    def add(self.product):
        product_id=str(medicine.id)
        #Logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id]={'price':str(medicine.price)}
        self.session.modified=True