from django.shortcuts import render, get_object_or_404
from .models import  Product, Category


def homepage(request):
    '''
        homepage - render all product in html pages
    '''
    products = Product.objects.filter(in_stock = True)
    return render(request, 'store/home.html', {'products': products})




# single product
def product_detail(request, slug):
    '''
    product-detail -> for return single page for product to ordering 
    '''
    product = get_object_or_404(Product, slug = slug, in_stock = True)
    return render(request, 'store/detail.html', {'product': product})


def category_product(request, category_slug):
    category = get_object_or_404(Category, slug = category_slug)
    products = Product.objects.filter(category = category)
    return render(request, 'store/c_product.html', {'category':category, 'products': products})