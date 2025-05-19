from django.shortcuts import get_object_or_404, render , redirect 
from django.urls import reverse
from django.http import Http404 , HttpResponse , JsonResponse
from .models import Product , Category , WishedProduct
from .froms import CommentForm
from django.utils.safestring import mark_safe
from django.db.models import Q 

# Create your views here.

def home(request):
    products = Product.objects.all().order_by("-count_rating")[:10]
    products_discount = Product.objects.all().order_by("-discount")[:12]
    return render(request, "shop/home.html",{"products":products,"d_products":products_discount})


def product_page(request, slug):
    product = Product.objects.filter(slug = slug).first()
    
    if product is not None:
        
        if request.method == 'POST':
            if request.user.is_authenticated:
                form = CommentForm(request.POST)
                if form.is_valid():
                    form.instance.product = product
                    form.instance.user = request.user
                    form.instance.rating = int(request.POST.get("rating"))
                    form.save()
                    return redirect(reverse("product",args=[product.slug]))
            else:
                return redirect("login")
        
        product.mini_description = mark_safe(product.mini_description)
    
        return render(request,"shop/product.html",{"product":product})
    
    else:
        return HttpResponse("not found")
    
    

def shop_page(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request,"shop/shop.html",{"products":products,"categories":categories})

def category_page(request,name):
    category = get_object_or_404(Category,name=name)
    
    return render(request,"shop/category.html",{"category":category})


def sale_page(request):
    products = Product.objects.all()
    
    return render(request,"shop/sale_page.html",{"products":products})

def wished_product(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.POST.get("action") == "post":
                product_id = request.POST.get("prId")
                
                product = Product.objects.filter(id = product_id).first()
                
                if product is not None:
                    wished = WishedProduct.objects.filter(product = product, user=request.user).first()
                    if wished is None:
                        WishedProduct.objects.create(product = product,user = request.user) 
                    
                        return JsonResponse({"message":"success"})
    
    return JsonResponse({"message":"nothing"})

def dis_wished(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.POST.get("action") == "post":
                wished_id = request.POST.get("prId")
                
                wished = WishedProduct.objects.filter(id=wished_id).first()
                
                if wished is not None:
                    wished.delete()
                    
                    return JsonResponse({"message":"success"})
    
    return JsonResponse({"message":"nothing"})

def search(request):
    search = request.GET.get("search")
    
    if search is not None:
    
        searcheds = Product.objects.filter(Q(name__contains = search )| Q(category__name__contains = search) | Q(mini_description__contains = search) | Q(factory__contains = search))
        
        return render(request,"shop/search.html",{"searcheds":searcheds,"search":search})
    
    return redirect("home")