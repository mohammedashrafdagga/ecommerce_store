from django.urls import path
from . import views


# app name
app_name = 'store'

# url path
urlpatterns = [
    path('', views.homepage, name='home'),
    path('c/<slug:category_slug>', views.category_product, name='category-product'),
    path('product/<slug:slug>', views.product_detail, name='product-detail'),
]

