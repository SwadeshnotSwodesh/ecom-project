import json
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import datetime
from .models import * 


def store(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cart_items = order.get_cart_items
    else:
        cart_items = 0

    products = Product.objects.all()
    context = {'products': products, 'cart_items': cart_items}
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
        cart_total = order.get_cart_items  # Total items in the cart
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart_total = 0

    context = {'items': items, 'order': order, 'cart_total': cart_total}
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



def delete_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data['itemId']
        order_item = OrderItem.objects.get(id=item_id)
        order_item.delete()

        return JsonResponse({'message': 'Item removed from cart!'}, safe=False)
    


def update_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data['itemId']
            action = data['action']

            # Get the order item
            order_item = OrderItem.objects.get(id=item_id)

            # Handle increment and decrement actions
            if action == 'increment':
                order_item.quantity += 1
            elif action == 'decrement' and order_item.quantity > 1:
                order_item.quantity -= 1

            order_item.save()  # Save the updated quantity
            return JsonResponse({'success': True, 'message': 'Quantity updated successfully!'}, safe=False)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, safe=False)
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
            order.save()

        if order.shipping:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print('User is not logged in')

    return JsonResponse('Payment submitted..', safe=False)