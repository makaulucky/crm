from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_orders = orders.count()
    total_customers = customers.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    cancelled = orders.filter(status='Out for delivery').count()

    context = {
        'orders': orders,
        'customers': customers,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'delivered': delivered,
        'pending': pending,
        'cancelled': cancelled
    }
    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

def customers(request, pk):
    customers = Customer.objects.get(id=pk)
    orders = customers.order_set.all()

    context = {
        'customers': customers,
        'orders': orders
    }
    return render(request, 'accounts/customer.html', context)

def accounts(request):
    return render(request, 'accounts/accounts.html')


def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form .is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form
    }
    return render(request, 'accounts/order_form.html', context)
