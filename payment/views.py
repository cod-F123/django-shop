from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.models import User
from .models import Order , OrderItem
from accounts.models import AddressUser , Profile
from cart.cart import Cart

# Create your views here.

def order_page(request,id):
    order = get_object_or_404(Order,id=id) 
    
    return render(request,"payment/order.html",{"order":order})

def checkout_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            address_list = AddressUser.objects.filter(user_id = request.user.id) 
            
            if address_list:
                
                return render(request,"payment/checkout.html",{"address_list":address_list})

            return redirect("my_account")
    
    return redirect("home")


def payment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            cart = Cart(request)
            products = cart.get_products()
            quantities = cart.get_quantities()
            
            address_id =request.POST.get("adrr")
            address = get_object_or_404(AddressUser,id=address_id)
            new_order = Order.objects.create(user = request.user,address = address,amount = cart.get_total())
            current_profile = Profile.objects.filter(user=request.user)
            current_profile.update(old_cart = "")
            
            for product in products:
                for key,value in quantities.items():
                    key = int(key)
                    
                    if key == product.id:
                        OrderItem.objects.create(order= new_order,product=product,user=request.user, quantity = value)
            
            for key in list(request.session.keys()):
                if "session_key" == key:
                    del request.session[key]
            
            
            return redirect("home")
    
    return redirect("home")


def pay_callback(request):
    pass