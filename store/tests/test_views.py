from unittest import skip
from store.models import Category, Product
from django.test import TestCase
from django.contrib.auth import get_user_model



User = get_user_model()


class TestViewMixin:
    def setUp(self):
        self.user = User.objects.create(username = 'test_user')
        self.category = Category.objects.create(name = 'django', slug = 'django')
        self.product = Product.objects.create(
            created_by = self.user,
            category = self.category,
            title = 'Django Framework',
            slug = 'django_framework',
            # image = 'media\product_images\University_Icon.jpg',
            price = 12.15
        )    
        
# Test View
