from django.urls import path 
from . import views 

urlpatterns = [
    path("checkout/",views.checkout_page,name="checkout"),
    path("pay/",views.payment,name="pay"),
    path("order/<int:id>/",views.order_page,name="order"),
]
