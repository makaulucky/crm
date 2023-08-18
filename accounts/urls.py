from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customers/<str:pk>/', views.customer, name='customer'),  # Updated function name
    path('accounts/', views.accounts, name='accounts'),
    path('create_order/', views.create_order, name='create_order'),  # Updated function name
    path('update_order/<str:pk>/', views.update_order, name='update_order'),  # Updated function name
    path('delete_order/<str:pk>/', views.delete_order, name='delete_order'),
    path('create_customer/', views.create_customer, name='create_customer'),
]
