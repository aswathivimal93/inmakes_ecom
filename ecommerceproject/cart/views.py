from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .models import Cart,CartItem,CartUserMapping
from shop.models import Product

from django.core.exceptions import ObjectDoesNotExist


def _cart_id(request):
    if request.user.is_authenticated:
        user_id=request.user.id
        if CartUserMapping.objects.filter(user=user_id):
            cart=CartUserMapping.objects.get(user=user_id).cart
        else:
            cart = request.session.session_key
            #CartUserMapping.objects.create(cart=cart,user=request.user)
            if not cart:
                cart = request.session.create()
            print(cart)
            #CartUserMapping.objects.create(cart=cart,user=request.user_id)
        #try:
         #   cartuser=CartUserMapping.objects.get(user=user_id)
         #   cart = cartuser.cart


       # except ObjectDoesNotExist:
           # cart = request.session.session_key
            #print(cart)
            #if cart:
             #   if not CartUserMapping.objects.filter(cart=cart, user=request.user).exists():
            #        CartUserMapping.objects.create(cart=cart, user=request.user)
            #if cart:
                #cartuser=CartUserMapping.objects.create(cart=cart,user=user_id)
            #else:
           # if not cart:
           #     cart = request.session.create()
                #cartuser = CartUserMapping.objects.create(cart=cart, user=user_id)
    else:
        cart=request.session.session_key
        if not cart:
            cart=request.session.create()
    return cart
def add_cart(request,product_id):
    product=Product.objects.get(id=product_id)

    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        print("cart exist")
        print(cart.id)
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
        print("does not exist")
        if request.user.is_authenticated:
            user= request.user
            if not CartUserMapping.objects.filter(cart=cart,user=user).exists():
                CartUserMapping.objects.create(cart=cart,user=user)
    try:
        cart_item=CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity<cart_item.product.stock:
            cart_item.quantity+=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()
    return redirect('cart:cart_detail')
def cart_detail(request,total=0,counter=0,cart_items=None):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,active=True)
        for cart_item in cart_items:
            total+=(cart_item.product.price*cart_item.quantity)
            counter+=cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request,'cart.html',dict(cart_items=cart_items,total=total,counter=counter))
def cart_remove(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity>1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:cart_detail')
def full_remove(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')




