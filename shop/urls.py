from django.urls import path 
from . import views 

urlpatterns = [
    path("",views.home, name="home"),
    path("product/<str:slug>/",views.product_page, name="product"),
    path("shop/",views.shop_page,name="shop"),
    path("category/<str:name>/",views.category_page,name="category"),
    path("sale/",views.sale_page,name="sale_products"),
    path("add-wish/",views.wished_product,name="add_wish"),
    path("dis-wish/",views.dis_wished,name="dis_wish"),
    path("search/",views.search,name="search")
]
