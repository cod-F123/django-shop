from django.shortcuts import render , redirect
from django.contrib.auth import login , logout , authenticate
from django.contrib import messages
from .forms import UserRegisterForm
from django.http import JsonResponse

# OTP
from .utils import send_email_to_user
from django.contrib.auth.models import User
import random

# Profile User
from .models import AddressUser
from .forms import AddressUserForm , UserProfileChange , ChangePAsswordUser

# cart
from cart.cart import Cart
from .models import Profile
import json

# Create your views here.

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request,user)
            
            current_user = Profile.objects.get(user__id = request.user.id)
            saved_cart = current_user.old_cart
            
            if saved_cart:
                saved_cart = json.loads(saved_cart)
                cart = Cart(request)
                
                for key , value in saved_cart.items():
                    cart.db_add(product=key,quantity=value)
                    
            
            return redirect("home")
        
        else:
            return redirect("login")
    
    return render(request,"accounts/login.html",{})


def logout_user(request):
    logout(request)
    
    return redirect("home")

users = {}
def create_code(email):
    user = users.get(email,None)
    if user is None:
        random_number = random.randint(10000,99999)
        
        users[email] = random_number
    
        return random_number
    
    return redirect("verifi_otp")

def verifi_otp(current_otp,otp):
    if current_otp == otp:
        return True
    else:
        return False

# Login with otp email
def login_with_otp(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        if user is not None:
            random_num = create_code(email)
            send_email_to_user("security code",random_num,[email])
            
            request.session["user_email_otp"] = email
            return redirect("verifi_otp")
            
    
    return render(request,"accounts/send_otp.html",{})

def verification_otp(request):
    if "user_email_otp" not in request.session:
        return redirect("send_otp")
    
    user = User.objects.get(email = request.session["user_email_otp"])
    
    user_otp = users.get(user.email)
    
    if request.method == 'POST':
        otp = request.POST.get("otp")
        
        verifi = verifi_otp(user_otp,otp)
        
        if verifi:
            login(request,user)
            return redirect("home")
    
    return render(request,"accounts/verifi_otp.html",{})


def register_user(request):
    if not request.user.is_authenticated:
        form = UserRegisterForm()
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            
            if form.is_valid():
                form.save()
                
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password2"]
                
                user = authenticate(username=username,password=password)
                
                if user is not None:
                    login(request,user)
                    return redirect("home")
            
            for error in list(form.errors.values()):
                messages.error(request,error)
                
            return redirect("login")
        
        return render(request,"accounts/login.html",{"form":form})
    
    else:
        return redirect("home")

def user_account(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_form = UserProfileChange(request.POST or None ,instance = request.user)
            if user_form.is_valid():
                user_form.save()
                return redirect("my_account")

            for error in list(user_form.errors.values()):
                messages.error(request,error)
        return render(request,"accounts/my-account.html",{})

    else:
        return redirect("login")

def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ChangePAsswordUser(request.user, request.POST or None)
            
            if form.is_valid():
                form.save()
                
                login(request,request.user)
                
                return redirect("home")
            for error in list(form.errors.values()):
                messages.error(request,error)
                
        return redirect("my_account")
    else:
        return redirect("login")
    

def add_address(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            address_form = AddressUserForm(request.POST)
            if address_form.is_valid():
                address_form.instance.user = request.user 
                address_form.save()
                
                return redirect("my_account")

        
        return redirect("my_account")
    else:
        return redirect("login")

def delete_address(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST.get("action") == 'post':
                addrss_id = request.POST.get("address")
                address = AddressUser.objects.filter(id = addrss_id)
                
                if address is not None:
                    address.delete()
                    return JsonResponse({"message":"success"})

                return JsonResponse({"message":"notfound"})
    
    
    return redirect("login")

def update_address(request,id):
    if request.user.is_authenticated:
        address = AddressUser.objects.filter(id=id).first()
        if request.method == 'POST':
            if address is not None:
                form_address = AddressUserForm(request.POST or None , instance= address)
                if form_address.is_valid():
                    form_address.save()
                    return redirect("my_account")
            else:
                return redirect("my_account")
                
    
        return render(request,"accounts/update-address.html",{"address":address})
    else:
        return redirect("login")
                