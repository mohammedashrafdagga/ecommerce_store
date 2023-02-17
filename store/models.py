from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()

# category table and Product
class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    
    
    class Meta:
        verbose_name_plural = 'categories'
        
    def __str__(self) -> str:
        return self.name

    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    created_by = models.ForeignKey(User, related_name='product_creator', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default='admin')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='product_images/')
    slug = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=4,decimal_places=2)
    in_stock = models.BooleanField(default=True)
    in_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-created',)
    
    # view single page for product - return url 
    @property
    def get_view_url(self):
        return reverse('store:product-detail', kwargs={'slug': self.slug})
    
    
    # return str method
    def __str__(self) -> str:
        return self.title