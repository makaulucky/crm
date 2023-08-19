from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('products/', views.products, name='products'),
    path('create_product/', views.create_product, name='create_product'),
    path('update_product/<str:pk>/', views.update_product, name='update_product'),
    path('delete_product/<str:pk>/', views.delete_product, name='delete_product'),
    path('customers/<str:pk>/', views.customer, name='customer'),
    path('accounts/', views.accounts, name='accounts'),
    path('create_order/<str:pk>/', views.create_order, name='create_order'),    
    path('update_order/<str:pk>/', views.update_order, name='update_order'),
    path('delete_order/<str:pk>/', views.delete_order, name='delete_order'),
    path('create_customer/', views.create_customer, name='create_customer'),
    path('update_customer/<str:pk>/', views.update_customer, name='update_customer'),
    path('delete_customer/<str:pk>/', views.delete_customer, name='delete_customer'),
]
