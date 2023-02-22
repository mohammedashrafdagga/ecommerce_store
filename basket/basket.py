


class Basket():
    
    
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('s_key')
        if 's_key' not in request.session:
            basket = self.session['s_key'] = {}
        self.basket = basket
        
        
    def add(self, product, product_qty):
        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id] = {'price': str(product.price), 'qty': product_qty}
        else:
            self.basket[product_id]['qty'] = self.basket[product_id]['qty'] + product_qty
        self.session.modified = True
        
        
    def __len__(self):
        return sum(item['qty'] for item in self.basket.values())