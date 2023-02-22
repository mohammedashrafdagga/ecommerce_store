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