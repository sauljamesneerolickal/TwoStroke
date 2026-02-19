from django.shortcuts import render, get_object_or_404
from inventory.models import Product, Category
from django.db.models import Q

def product_catalog(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    
    products = Product.objects.filter(is_active=True, stock_quantity__gt=0)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(vehicle_model__icontains=query) | 
            Q(code__icontains=query)
        )
        
    if category_id:
        products = products.filter(category_id=category_id)
        
    categories = Category.objects.all()
    
    return render(request, 'catalog/catalog.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': int(category_id) if category_id else None
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    return render(request, 'catalog/product_detail.html', {'product': product})
