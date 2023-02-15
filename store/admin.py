from django.contrib import admin
from .models import Category, Product


# Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}
    
    
# Product Admin created
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author','price','in_stock']
    list_editable = ['price', 'in_stock']
    list_filter = ['in_stock', 'in_active']
    prepopulated_fields = {'slug': ('title', )}