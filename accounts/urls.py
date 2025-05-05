from django.urls import path 
from . import views 

urlpatterns = [
    path("login/",views.login_user,name="login"),
    path("logout/",views.logout_user,name="logout"),
    path("send_otp/",views.login_with_otp, name="send_otp"),
    path("verifi_otp/",views.verification_otp,name="verifi_otp"),
    path("register/",views.register_user,name="register")
]
