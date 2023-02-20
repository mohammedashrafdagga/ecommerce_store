from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def homepage(request):
    '''
        homepage - render all product in html pages
    '''
    products = Product.products.all()
    return render(request, 'store/home.html', {'products': products})




# single product
def product_detail(request, slug):
    '''
        product-detail -> for return single page for product to ordering 
    '''
    product = get_object_or_404(Product, slug = slug, in_stock = True)
    return render(request, 'store/product_detail.html', {'product': product})


def category_product(request, category_slug):
    category = get_object_or_404(Category, slug = category_slug)
    products = Product.products.filter(category = category)
    return render(request, 'store/category_product.html', {'category': category, 'products': products})