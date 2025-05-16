from django.shortcuts import render , redirect , get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Order , OrderItem
from accounts.models import AddressUser , Profile
from cart.cart import Cart
from django.contrib import messages
import uuid  
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings

# Create your views here.

PAYPAL_RECEIVER_EMAIL = settings.PAYPAL_RECEIVER_EMAIL

def order_page(request,id):
    order = get_object_or_404(Order,id=id) 
    if order.user.id == request.user.id:
        invoice = uuid.uuid4()
        
        order.invoice = str(invoice)
        order.save()
        
        paypal_dict = {
            "business" : PAYPAL_RECEIVER_EMAIL,
            "amount" : str(order.amount),
            "item_name": "Product",
            "invoice": str(invoice),
            "currency_code": "USD",
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return_url": request.build_absolute_uri(reverse('payment-success')),
            "cancel_return": request.build_absolute_uri(reverse('payment-cancel')),
        }
        
        form = PayPalPaymentsForm(initial=paypal_dict)
        
        return render(request,"payment/order.html",{"order":order,"form":form})
    
    messages.success(request,"Access Diend !")

    return redirect("home")



def checkout_page(request):
    if request.user.is_authenticated:
        if len(Cart(request)) != 0:
            if request.method == 'POST':
                address_list = AddressUser.objects.filter(user_id = request.user.id) 
                
                if address_list:
                    
                    return render(request,"payment/checkout.html",{"address_list":address_list})

                return redirect("my_account")
        
    messages.success(request,"Access Diend !")
    
    return redirect("home")


def payment_new_order(request):
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
            
            return redirect(reverse("order",args=[new_order.id]))
                        
            
    messages.success(request,"Access Diend !")
    return redirect("home")


def paymetn_success(request):
    payer_id = request.GET.get("PayerID")
    
    order = Order.objects.filter(payer_id = payer_id).first()
    
    return render(request,"payment/payment-success.html",{"order":order})

def payment_cancel(request):
    return render(request,"payment/payment-cancel.html")