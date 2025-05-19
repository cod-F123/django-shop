from django.urls import path , include
from . import views 

urlpatterns = [
    path("checkout/",views.checkout_page,name="checkout"),
    path("pay/new-order",views.payment_new_order,name="pay"),
    path("order/<int:id>/",views.order_page,name="order"),
    path('payment-success/', views.paymetn_success, name='payment-success'),
    path('payment-cancel/', views.payment_cancel, name='payment-cancel'),
    path('paypal/', include("paypal.standard.ipn.urls")),
]
