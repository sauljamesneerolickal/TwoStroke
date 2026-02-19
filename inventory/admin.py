from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'seller', 'category', 'price', 'stock_quantity', 'is_active')
    list_filter = ('category', 'seller', 'is_active')
    search_fields = ('name', 'code', 'vehicle_model')
