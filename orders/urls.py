from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.order_create, name='checkout'),
    path('seller/orders/', views.seller_order_list, name='seller_order_list'),
    path('detail/<str:order_id>/', views.order_detail, name='order_detail'),
    path('update-status/<str:order_id>/', views.update_order_status, name='update_order_status'),
]
