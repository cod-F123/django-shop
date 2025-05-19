from django.shortcuts import render , redirect , get_object_or_404
from django.urls import reverse
from payment.models import Order
from .filters import OrderFilter , UserFilter
from django.contrib.auth.models import User
from .froms import UserUpdateForm

# Permission
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied

# Create your views here.

def dashboard(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        orders = Order.objects.all().order_by("-date_ordered")[:7]
        users = User.objects.all().order_by("date_joined").order_by("-date_joined")[:7]
        
        return render(request,"dashboard/dashboard.html",{"orders":orders,"users":users})
    
    return redirect("home")

def order_dashboard(request):
    if request.user.is_authenticated and (request.user.is_staff , request.user.is_superuser):
        queryset = Order.objects.all().select_related("user")
        order_filter = OrderFilter(request.GET,queryset=queryset)
        
        return render(request,"dashboard/order_dashboard.html",{"filter":order_filter,"orders":order_filter.qs})
    return redirect("home")


def detail_order_dashboard(request,id):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        order = get_object_or_404(Order, id = id)
        
        if request.method == "POST":
            if request.user.has_perm("payemnt.change_order"):
                order_status = request.POST.get("order_status")
                
                order.order_status = order_status
                order.save()
                return redirect(reverse("D_order",args=[order.id]))
        
        
        return render(request,"dashboard/order.html",{"order":order})

    return redirect("home")


def user_dashboard(request):
    if request.user.is_authenticated and (request.user.is_staff , request.user.is_superuser):
        queryset = User.objects.all().order_by("-date_joined")
        user_filter = UserFilter(request.GET,queryset=queryset)
        
        return render(request,"dashboard/user_dashboard.html",{"filter":user_filter,"users":user_filter.qs})
    return redirect("home")


@permission_required(["auth.view_user"],raise_exception=True)
def detail_user_dashboard(request,id):
    user = get_object_or_404(User,id = id) 
    if request.method == "POST":
        if request.user.has_perm("auth.change_user"):
            user_form = UserUpdateForm(request.POST or None,instance = user)
            
            if user_form.is_valid():
                user_form.save()
                return redirect(reverse("D_user",args=[user.id]))
            
        return redirect(reverse("D_user",args=[user.id]))
    
    return render(request,"dashboard/user.html",{"user_":user})