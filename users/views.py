from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .forms import CustomerRegistrationForm, SellerRegistrationForm, SpareTrackLoginForm, UserProfileForm, AdminUserCreationForm

def home(request):
    return render(request, 'home.html')

def register_view(request):
    return render(request, 'users/register_choice.html')

def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to SpareTrack.")
            return redirect('customer_dashboard')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'users/register.html', {'form': form, 'role': 'Customer'})

def register_seller(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.info(request, "Registration successful! Your seller account is pending admin approval.")
            return redirect('login')
    else:
        form = SellerRegistrationForm()
    return render(request, 'users/register.html', {'form': form, 'role': 'Seller'})

def login_view(request):
    if request.user.is_authenticated:
        return redirect_role_based(request.user)
        
    if request.method == 'POST':
        form = SpareTrackLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.role == 'seller' and not user.is_approved:
                    messages.warning(request, "Your seller account is still pending approval.")
                    return redirect('login')
                login(request, user)
                return redirect_role_based(user)
        else:
            # Form is invalid - could be wrong password OR blocked user (since authenticate() fails for blocked users)
            username = form.data.get('username')
            password = form.data.get('password')
            
            if username and password:
                try:
                    user_chk = User.objects.get(username=username)
                    if user_chk.check_password(password):
                        if not user_chk.is_active:
                            messages.error(request, "Your account has been blocked by the administrator.")
                        else:
                            messages.error(request, "Invalid username or password.")
                    else:
                        messages.error(request, "Invalid username or password.")
                except User.DoesNotExist:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid login details.")
    else:
        form = SpareTrackLoginForm()
    return render(request, 'users/login.html', {'form': form})

def redirect_role_based(user):
    if user.role == 'customer':
        return redirect('customer_dashboard')
    elif user.role == 'seller':
        return redirect('seller_dashboard')
    elif user.role == 'admin':
        return redirect('admin_dashboard')
    return redirect('home')

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')

@login_required
def customer_dashboard(request):
    if request.user.role != 'customer':
        return redirect('home')
    return render(request, 'catalog/dashboard.html')

@login_required
def seller_dashboard(request):
    if request.user.role != 'seller' or not request.user.is_approved:
        return redirect('home')
    return render(request, 'inventory/dashboard.html')

from django.db.models import Sum, Count, Avg
from django.utils import timezone
from inventory.models import Product, Category
from orders.models import Order

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('home')
    
    stats = {
        'total_customers': User.objects.filter(role='customer').count(),
        'total_sellers': User.objects.filter(role='seller').count(),
        'total_products': Product.objects.count(),
        'total_orders': Order.objects.count(),
        'total_revenue': Order.objects.aggregate(Sum('total_paid'))['total_paid__sum'] or 0,
        'sales_today': Order.objects.filter(created_at__date=timezone.now().date()).aggregate(Sum('total_paid'))['total_paid__sum'] or 0,
        'low_stock_count': Product.objects.filter(stock_quantity__lte=5).count(),
    }
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    return render(request, 'users/admin/dashboard.html', {'stats': stats, 'recent_orders': recent_orders})

@login_required
def admin_users(request):
    if request.user.role != 'admin':
        return redirect('home')
    all_users = User.objects.exclude(role='admin').order_by('-date_joined')
    return render(request, 'users/admin/users.html', {'all_users': all_users})

@login_required
def admin_add_user(request):
    if request.user.role != 'admin':
        return redirect('home')
    
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"New user '{user.username}' created successfully.")
            return redirect('admin_users')
    else:
        form = AdminUserCreationForm()
        
    return render(request, 'users/admin/add_user.html', {'form': form})

@login_required
def admin_products(request):
    if request.user.role != 'admin':
        return redirect('home')
    categories = Category.objects.all().annotate(product_count=Count('products'))
    low_stock_items = Product.objects.filter(stock_quantity__lte=5).order_by('stock_quantity')
    return render(request, 'users/admin/products.html', {'categories': categories, 'low_stock_items': low_stock_items})

@login_required
def admin_orders(request):
    if request.user.role != 'admin':
        return redirect('home')
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'users/admin/orders.html', {'orders': orders})

@login_required
def admin_reports(request):
    if request.user.role != 'admin':
        return redirect('home')
    stats = {
        'total_revenue': Order.objects.aggregate(Sum('total_paid'))['total_paid__sum'] or 0,
        'avg_order_value': Order.objects.all().aggregate(avg=Avg('total_paid'))['avg'] or 0,
        'orders_count': Order.objects.count(),
    }
    return render(request, 'users/admin/reports.html', {'stats': stats})

@login_required
def admin_settings(request):
    if request.user.role != 'admin':
        return redirect('home')
    return render(request, 'users/admin/settings.html')

@login_required
def approve_seller(request, user_id):
    if request.user.role != 'admin':
        return redirect('home')
    seller = get_object_or_404(User, id=user_id, role='seller')
    seller.is_approved = True
    seller.save()
    messages.success(request, f"Seller {seller.username} has been approved.")
    return redirect('admin_users')

@login_required
def toggle_user_status(request, user_id):
    if request.user.role != 'admin':
        return redirect('home')
    user = get_object_or_404(User, id=user_id)
    if user.is_active:
        user.is_active = False
        messages.warning(request, f"User {user.username} has been blocked.")
    else:
        user.is_active = True
        messages.success(request, f"User {user.username} has been reactivated.")
    user.save()
    return redirect('admin_users')

@login_required
def delete_user(request, user_id):
    if request.user.role != 'admin':
        return redirect('home')
    user = get_object_or_404(User, id=user_id)
    username = user.username
    user.delete()
    messages.success(request, f"User {username} has been removed from the system.")
    return redirect('admin_users')

@login_required
def admin_profile(request):
    if request.user.role != 'admin':
        return redirect('home')
    
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('admin_profile')
        
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed successfully!")
                return redirect('admin_profile')
            else:
                profile_form = UserProfileForm(instance=request.user)
                return render(request, 'users/admin_profile.html', {
                    'profile_form': profile_form,
                    'password_form': password_form
                })
    
    profile_form = UserProfileForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)
    
    return render(request, 'users/admin_profile.html', {
        'profile_form': profile_form,
        'password_form': password_form
    })
