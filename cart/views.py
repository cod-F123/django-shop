from django.shortcuts import render , get_object_or_404 , redirect
from .cart import Cart
from shop.models import Product
from django.http import JsonResponse

# Create your views here.

def cart_page(request):
    cart = Cart(request)
    products = cart.get_products()
    quantities = cart.get_quantities()
    total = cart.get_total()
    
    return render(request,"cart/cart.html",{"products":products,"quantities":quantities,"total":total})

def add_cart(request):
    if request.method == 'POST':
        if request.POST.get("action") == 'post':
            cart = Cart(request)
            pr_id = request.POST.get("proId")
            pr_qty = request.POST.get("proQty")
            
            # Get product
            product = get_object_or_404(Product,id=pr_id) 
            if pr_qty is not None:
                cart.add(product,pr_qty)
            
            else:
                cart.add(product,1)
        
            cart_qty = len(cart)
            
            return JsonResponse({"cart_len":cart_qty})
            

def delete_item(request):
    if request.method == 'POST':
        if request.POST.get("action") == 'post':
            cart = Cart(request)
            product_id = request.POST.get("proId")
            
            product = get_object_or_404(Product,id = product_id)
            
            cart.delete(product)
            
            cart_len = len(cart)
            total  = cart.get_total()
            
            return JsonResponse({"cart_len":cart_len,"total":total})


def update_cart(request):
    if request.method == 'POST':
        if request.POST.get("action") == 'post':
            cart = Cart(request)
            product_id = request.POST.get("proId")
            quantity = request.POST.get("proQty")
            
            product = get_object_or_404(Product,id = product_id)
            
            cart.update(product,quantity)
            
            cart_len = len(cart)
            total  = cart.get_total()
            
            return JsonResponse({"total":total})
        
        
def clear_cart(request):
    if request.method == 'POST':
        cart = Cart(request)
        cart.clear()
        
        return redirect("home")
    
    return redirect("home")