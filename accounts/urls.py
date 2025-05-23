from django.urls import path 
from . import views 

urlpatterns = [
    path("login/",views.login_user,name="login"),
    path("logout/",views.logout_user,name="logout"),
    path("send_otp/",views.login_with_otp, name="send_otp"),
    path("verifi_otp/",views.verification_otp,name="verifi_otp"),
    path("register/",views.register_user,name="register"),
    path("",views.user_account,name="my_account"),
    path("change-password/",views.change_password,name="change_password"),
    path("add-address/",views.add_address,name="add_address"),
    path("delete-address/",views.delete_address,name= "delete_address"),
    path("update-address/<int:id>/",views.update_address,name="update_address"),
]
