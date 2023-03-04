from store.models import Product
from decimal import Decimal

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
        self.save()
        
    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.products.filter(id__in = product_ids)
        basket = self.basket.copy()
        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def delete(self, product_id):
        # if founded remove
        if product_id in self.basket.keys():
            del self.basket[product_id]
        self.save()
        
    def update(self, product_id, product_qty):
        if product_id in self.basket.keys():
            self.basket[product_id]['qty'] = product_qty
            
        self.save()
    
    
    def save(self):
        self.session.modified = True
    
    def __len__(self):
        return sum(item['qty'] for item in self.basket.values())    
    
    
    # get total price
    
    def get_product_total(self, product_id) -> str:
        price = Decimal(self.basket[product_id]['price'])
        total =  self.basket[product_id]['qty'] * price
        return total
    
    
    
    def get_total_price(self) -> str:
        total =  sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
        return total