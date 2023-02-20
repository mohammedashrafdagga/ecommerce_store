
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from store.models import Category, Product

User = get_user_model()


class TestViewMixin:
    def setUp(self):
        self.user = User.objects.create(username = 'test_user')
        self.category = Category.objects.create(name = 'django', slug = 'django')
        self.category1 = Category.objects.create(name = 'python', slug = 'python')
        self.product = Product.objects.create(
            created_by = self.user,
            category = self.category,
            title = 'Django Framework',
            slug = 'django_framework',
            price = 12.15
        )
        self.product1 = Product.objects.create(
            created_by = self.user,
            category = self.category1,
            title = 'Python Framework',
            slug = 'python_framework',
            price = 12.15,
            in_stock = False
        )
        self.client = Client()
        
# Test View
class TestProductView(
    TestViewMixin,
    TestCase
    ):

    def test_homepage(self):
        '''
            Test HomePage redirect (url) -> '/' 
            homepage method -> url_name = 'home'
        '''
        # get response
        response = self.client.get(reverse('store:home'))
        # assert status code
        self.assertEqual(response.status_code, 200)
        # assert template used
        self.assertTemplateUsed(response, 'store/home.html')
        # assert context return by homepage
        context = response.context
        self.assertEqual(len(context['products']), 1)
        self.assertEqual(len(context['categories']), 2)

    
    def test_detail_not_in_stock(self):
        '''
            we test detail product page -> product/<slug:slug>/
            product_detail > product-name
            with slug
        '''
        # get response
        response = self.client.get(reverse('store:product-detail', kwargs={'slug':self.product1.slug}))
        # assert status code
        self.assertEqual(response.status_code, 404)


    def test_detail_in_stock(self):
        '''
            we test detail product page -> product/<slug:slug>/
            product_detail > product-name
            with slug
        '''
        # get response
        response = self.client.get(reverse('store:product-detail', kwargs={'slug':self.product.slug}))
        # assert status code
        self.assertEqual(response.status_code, 200)
        # assert template used 
        self.assertTemplateUsed(response, 'store/detail.html')
        # assert context return by homepage
        context = response.context
        # return one item and the item is instance from Product
        self.assertIsInstance(context['product'], Product)
        # and the title is equal the title of product build ion steUp Method 
        self.assertEqual(context['product'].title, self.product.title)

    
    # category product
    def test_category_product_not_found(self):
        '''
            we test the view category_product and the 
            path -> /category_slug/ -> the return all product in category define
        '''
        response = self.client.get(reverse('store:category-product', kwargs={'category_slug': 'learning'}))
        # the view must return the 404 response status code
        self.assertEqual(response.status_code, 404)
        
        # category product
    def test_category_product_found(self):
        '''
            we test the view category_product and the 
            path -> /category_slug/ -> the return all product in category define
        '''
        response = self.client.get(reverse('store:category-product', kwargs={'category_slug': self.category}))
        # assert status code
        self.assertEqual(response.status_code, 200)
        # assert template used
        self.assertTemplateUsed(response, 'store/c_product.html')
        # assert context return by homepage
        context = response.context
        # this category have one product, so the view must return len of product is 1
        self.assertEqual(len(context['products']), 1)
        #  he check the category return is same sended or not by check name of category
        self.assertEqual(context['category'].name, self.category.name)
