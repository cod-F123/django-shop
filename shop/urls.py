from django.urls import path 
from . import views 

urlpatterns = [
    path("",views.home, name="home"),
    path("product/<str:slug>/",views.product_page, name="product")
]
