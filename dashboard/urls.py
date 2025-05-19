from django.urls import path 
from . import views 

urlpatterns = [
    path("",views.dashboard,name="dashboard"),
    path("orders/",views.order_dashboard,name="order_dashboard"),
    path("orders/<int:id>/",views.detail_order_dashboard,name="D_order"),
    path("users/",views.user_dashboard,name="user_dashboard"),
    path("users/<int:id>/",views.detail_user_dashboard,name="D_user"),
]
