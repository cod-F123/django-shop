from django.urls import path 
from . import views 

urlpatterns = [
    path("",views.cart_page,name="cart"),
    path("add-cart/",views.add_cart,name="add_cart"),
    path("delete-cart/",views.delete_item,name="delete_cart"),
    path("update-cart/",views.update_cart,name="update_cart"),
    path("clear-cart/",views.clear_cart,name="clear_cart"),
]
