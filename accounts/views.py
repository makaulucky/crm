from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


from .models import *
from .forms import *
from .filters import *
from .decorators import *


@unauthenticated_user
def register(request):   
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name = 'Customer')

            user.groups.add(group)

            Customer.objects.create(user=user)

            messages.success(request, 'Account was created for ' + username)
            
            return redirect('login')
        
    context = {
        'form': form
    }
    return render (request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
    username = ''
    password = ''

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incorrect')

    context = {
            'username': username,
            'password': password
        }

    return render (request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_orders = orders.count()
    total_customers = customers.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    out_for_delivery = orders.filter(status='Out for delivery').count()  # Corrected status

    context = {
        'orders': orders,
        'customers': customers,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'delivered': delivered,
        'pending': pending,
        'out_for_delivery': out_for_delivery  # Updated variable name
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users (allowed_roles=['Customer'])
def user_page(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()    
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    out_for_delivery = orders.filter(status='Out for delivery').count() 
    
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
        'out_for_delivery': out_for_delivery
    }
    return render(request, 'accounts/user.html',context)

@login_required(login_url='login')
@allowed_users (allowed_roles=['Admin', 'Staff'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

@login_required(login_url='login')
@allowed_users (allowed_roles=['Admin', 'Staff'])
def create_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'accounts/product_form.html', context)

@login_required(login_url='login')
@allowed_users (allowed_roles=['Admin', 'Staff'])
def update_product(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'accounts/product_form.html', context)

@login_required(login_url='login')
@allowed_users (allowed_roles=['Admin', 'Staff'])
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('/')
    context = {
        'item': product
    }
    return render(request, 'accounts/delete.html', context)

@login_required(login_url='login')
@allowed_users (allowed_roles=['Admin', 'Staff'])
def customer(request, pk): 
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    

    myFilter= OrderFilter(request.GET, queryset=orders)
    orders=myFilter.qs
    
    context = {
        'customer': customer,
        'orders': orders,
        'myFilter': myFilter
    }
    return render(request, 'accounts/customer.html', context)
@login_required(login_url='login')
@allowed_users (allowed_roles=['Admin', 'Staff'])
def create_customer(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'accounts/customer_form.html', context)
@login_required(login_url='login')
@allowed_users (allowed_roles=['Admin', 'Staff'])
def update_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form
    }
    return render(request, 'accounts/customer_form.html', context)

@login_required(login_url='login')
@allowed_users (allowed_roles=['Admin', 'Staff'])
def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('/')
    context = {
        'item': customer
    }
    return render(request, 'accounts/delete.html', context)

@login_required(login_url='login')
@allowed_users (allowed_roles=['Admin', 'Staff'])
def accounts(request):
    return render(request, 'accounts/accounts.html')

@login_required(login_url='login')
@allowed_users (allowed_roles=['Admin', 'Staff'])
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    #form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {
        'formset': formset
    }
    return render(request, 'accounts/order_form.html', context)
@login_required(login_url='login')
@allowed_users (allowed_roles=['Admin', 'Staff'])
def update_order(request, pk): 
    order = Order.objects.get(id=pk)
    #form = OrderForm(instance=order)
    formset = OrderForm(instance=order)
    
    if request.method == 'POST':
        #form = OrderForm(request.POST, instance=order)
        formset = OrderForm(request.POST, instance=order)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {
        'formset': formset
    }
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users (allowed_roles=['Admin', 'Staff'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {
        'item': order
    }
    return render(request, 'accounts/delete.html', context)

@login_required(login_url='login')
def account_settings(request):
    return render(request, 'accounts/accounts.html')
