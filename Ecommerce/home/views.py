from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import datetime
import json
# Create your views here.
def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping' : False}
        cartItems = order['get_cart_items']


    products = Product.objects.all
    context = {'products' :products, 'cartItems': cartItems}
    return render(request , 'index.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping' : False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order':order, 'cartItems': cartItems}
    return render(request , 'cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping' : False}
        cartItems = order['get_cart_items']
    if 'perform' in request.POST:
         address = request.POST.get('address')
         city = request.POST.get('city')
         state = request.POST.get('state')
         zipcode = request.POST.get('zipcode')

         shippingadress = ShippingAddress(address=address, city=city, state=state, zipcode=zipcode)
         shippingadress.save()

    context = {'items': items, 'order':order, 'cartItems':cartItems}  
    return render(request , 'chechout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	# transaction_id = datetime.datetime.now().timestamp()
	# data = json.loads(request.body)

	# if request.user.is_authenticated:
	# 	customer = request.user.customer
	# 	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	# 	total = float(data['form']['total'])
	# 	order.transaction_id = transaction_id

	# 	if total == order.get_cart_total:
	# 		order.complete = True
	# 	order.save()

	# 	if order.shipping == True:
	# 		ShippingAddress.objects.create(
	# 		customer=customer,
	# 		order=order,
	# 		address=data['shipping']['address'],
	# 		city=data['shipping']['city'],
	# 		state=data['shipping']['state'],
	# 		zipcode=data['shipping']['zipcode'],
	# 		)
	# else:
	# 	print('User is not logged in')

	return JsonResponse('Payment submitted..', safe=False)

def contact(request):
    if 'submit' in request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        contact = Contact(name=name, email=email, message=message)
        contact.save() 
        # return render(f"{name} : Message is send...")
    return render(request, 'index.html' , {'Message': f'{name:} Message Send....'})