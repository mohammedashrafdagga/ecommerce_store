from django.contrib.auth import get_user_model
from django.test import TestCase

from store.models import Category, Product

User = get_user_model()


# Mixin
class CategoryMixin:
    def setUp(self) -> None:
        self.user = User.objects.create(username = 'test_user')
        self.category = Category.objects.create(name = 'django', slug = 'django')
        

class ProductMixin(CategoryMixin):
    def setUp(self) -> None:
        super().setUp()
        self.product = Product.objects.create(
            created_by = self.user,
            category = self.category,
            title = 'Django Framework',
            slug = 'django_framework',
            price = 12.15
        )

class CategoryTestCase(CategoryMixin, TestCase):
    '''
     Test __str__  Method in Category Model Class
     
    '''
    def test__str__(self):
        self.assertEqual(str(self.category), 'django')
    
    
    
class ProductTestCase(ProductMixin, TestCase):
      
    def test_str_(self):
        self.assertEqual(str(self.product), 'Django Framework')
       