from django.shortcuts import render, get_object_or_404
from .basket import Basket
from store.models import Product
from django.http import JsonResponse
# Create your views here.

def basket_summary(request):
    
    return render(request, 'basket/summary.html')



def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id = product_id)
        # add to basket
        basket.add(product=product, product_qty = product_qty)
    basket_qty = basket.__len__()
    
    response = JsonResponse(
        {'qty': basket_qty}
    )
    return response



def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        basket.delete(product_id = product_id)
    basket_qty = basket.__len__()
    basket_total = basket.get_total_price()
    return JsonResponse({'qty': basket_qty, 'basket_total': basket_total})





# update method 
def basket_update(request):
    basket = Basket(request)
    product_id = request.POST.get('product_id')
    if request.POST.get('action') == 'put':
        # get product id and new qty
        product_qty = int(request.POST.get('product_qty'))
        
        # update item
        basket.update(product_id, product_qty)
    basket_qty = basket.__len__()
    basket_total = basket.get_total_price()
    total_price = basket.get_product_total(product_id)
    print(total_price)
    response = {'qty' : basket_qty,
                         'total_price':total_price,
                         'basket_total': basket_total}
    print(response)
    return JsonResponse(response)