from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from inventory.models import Product
from .cart import Cart
from .models import OrderItem, Order
from .forms import OrderCreateForm
import uuid

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity)
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'orders/cart_detail.html', {'cart': cart})

@login_required
def order_create(request):
    cart = Cart(request)
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('product_catalog')
        
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_paid = cart.get_total_price()
            order.order_id = str(uuid.uuid4()).split('-')[0].upper()
            order.save()
            
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                # Reduce stock
                product = item['product']
                product.stock_quantity -= item['quantity']
                product.save()
                
            cart.clear()
            messages.success(request, f"Order {order.order_id} placed successfully!")
            return render(request, 'orders/order_success.html', {'order': order})
    else:
        form = OrderCreateForm(initial={'full_name': request.user.get_full_name(), 'email': request.user.email})
    return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})

@login_required
def seller_order_list(request):
    if request.user.role != 'seller':
        return redirect('home')
    # Finding orders that contain products from this seller
    orders = Order.objects.filter(items__product__seller=request.user).distinct().order_by('-created_at')
    return render(request, 'orders/seller_orders.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    # Check if user is the buyer or a seller of one of the items
    is_seller = order.items.filter(product__seller=request.user).exists()
    if request.user != order.user and not is_seller:
        return redirect('home')
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def update_order_status(request, order_id):
    if request.user.role != 'seller':
        return redirect('home')
    order = get_object_or_404(Order, order_id=order_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Order.STATUS_CHOICES):
            order.status = status
            order.save()
            messages.success(request, f"Order {order.order_id} status updated to {status.capitalize()}.")
    return redirect('seller_order_list')
