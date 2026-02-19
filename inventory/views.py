from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category
from .forms import ProductForm

@login_required
def product_list(request):
    if request.user.role != 'seller':
        return redirect('home')
    products = Product.objects.filter(seller=request.user)
    return render(request, 'inventory/dashboard.html', {'products': products})

@login_required
def product_add(request):
    if request.user.role != 'seller':
        return redirect('home')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, f"Product '{product.name}' added successfully.")
            return redirect('seller_dashboard')
    else:
        form = ProductForm()
    return render(request, 'inventory/product_form.html', {'form': form, 'title': 'Add New Product'})

@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{product.name}' updated successfully.")
            return redirect('seller_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/product_form.html', {'form': form, 'title': 'Edit Product'})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, f"Product '{product.name}' deleted.")
        return redirect('seller_dashboard')
    return render(request, 'inventory/product_confirm_delete.html', {'product': product})
