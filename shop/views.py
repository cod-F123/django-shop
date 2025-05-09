from django.shortcuts import render , redirect
from django.http import Http404 , HttpResponse
from .models import Product
from .froms import CommentForm
from django.utils.safestring import mark_safe

# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request, "shop/home.html",{"products":products})


def product_page(request, slug):
    product = Product.objects.filter(slug = slug).first()
    
    if product is not None:
        
        if request.method == 'POST':
            if request.user.is_authenticated:
                form = CommentForm(request.POST)
                if form.is_valid():
                    form.instance.product = product
                    form.instance.user = request.user
                    form.save()
            else:
                return redirect("login")
        
        product.mini_description = mark_safe(product.mini_description)
    
        return render(request,"shop/product.html",{"product":product})
    
    else:
        return HttpResponse("not found")
    
    

def shop_page(request):
    products = Product.objects.all()
    return render(request,"shop/shop.html",{"products":products})