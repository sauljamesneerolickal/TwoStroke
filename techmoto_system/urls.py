from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

urlpatterns = [
    path('admin_django/', admin.site.urls), # Django's built-in admin
    
    path('', user_views.home, name='home'),
    path('login/', user_views.login_view, name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    path('register/', user_views.register_view, name='register'),
    path('register/customer/', user_views.register_customer, name='register_customer'),
    path('register/seller/', user_views.register_seller, name='register_seller'),
    
    path('customer/', user_views.customer_dashboard, name='customer_dashboard'),
    path('seller/', user_views.seller_dashboard, name='seller_dashboard'),
    path('admin/', user_views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/', user_views.admin_users, name='admin_users'),
    path('admin/add-user/', user_views.admin_add_user, name='admin_add_user'),
    path('admin/products/', user_views.admin_products, name='admin_products'),
    path('admin/orders/', user_views.admin_orders, name='admin_orders'),
    path('admin/reports/', user_views.admin_reports, name='admin_reports'),
    path('admin/settings/', user_views.admin_settings, name='admin_settings'),
    path('admin/profile/', user_views.admin_profile, name='admin_profile'),
    path('admin/approve-seller/<int:user_id>/', user_views.approve_seller, name='approve_seller'),
    path('admin/toggle-user/<int:user_id>/', user_views.toggle_user_status, name='toggle_user_status'),
    path('admin/delete-user/<int:user_id>/', user_views.delete_user, name='delete_user'),
    
    # Internal app urls
    path('catalog/', include('catalog.urls')),
    path('inventory/', include('inventory.urls')),
    path('orders/', include('orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
