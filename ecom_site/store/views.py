import json
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import * 

def store(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'store/store.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('store')  # Redirect to the store page
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'store/register.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)



def checkout(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}

    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)



def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data['productId']
        product = Product.objects.get(id=product_id)

        if request.user.is_authenticated:
            customer, created = Customer.objects.get_or_create(user=request.user)
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
            order_item.quantity += 1
            order_item.save()

            cart_total = order.get_cart_items
            return JsonResponse({'message': 'Item added to cart!', 'cartTotal': cart_total}, safe=False)
        else:
            return JsonResponse({'message': 'You need to log in to add items to the cart.'}, safe=False)
        


def product_view(request, id):
    product = get_object_or_404(Product, id=id)
    context = {'product': product}
    return render(request, 'store/product_view.html', context)
