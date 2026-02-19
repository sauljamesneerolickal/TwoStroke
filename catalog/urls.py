from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_catalog, name='product_catalog'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]
