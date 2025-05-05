from django.shortcuts import render , redirect
from django.contrib.auth import login , logout , authenticate
from django.contrib import messages
from .forms import UserRegisterForm

# OTP
from .utils import send_email_to_user
from django.contrib.auth.models import User
import random

# Create your views here.

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request,user)
            
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
        print(users)
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
                
            return redirect("login")
        
        return render(request,"accounts/login.html",{"form":form})