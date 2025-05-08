from shop.models import Product
from accounts.models import Profile
import json 


class Cart:
    def __init__(self,request):
        self.session = request.session
        self.request = request
        
        cart = self.session.get("session_key")
        
        if "session_key" not in self.session:
            cart = self.session["session_key"] = {}
        
        self.cart = cart 
    
    
    def db_add(self, product, quantity):
        product_id = str(product) 
        
        if product_id not in self.cart:
            self.cart[product_id] = int(quantity)
        
        self.session.modified = True
        
        if self.request.user.is_authenticated:
            user_profile = Profile.objects.filter(user__id = self.request.user.id)
            
            current_cart = str(self.cart)
            current_cart = current_cart.replace("\'","\"")
            
            user_profile.update(old_cart = current_cart)
            
        
    def add(self, product, quantity):
        product_id = str(product.id)
        
        if product_id not in self.cart.keys():
            self.cart[product_id] = quantity
            
        self.session.modified = True 
        
        if self.request.user.is_authenticated:
            user_profile = Profile.objects.filter(user__id = self.request.user.id)
            
            current_cart = str(self.cart)
            current_cart = current_cart.replace("\'","\"")
            
            user_profile.update(old_cart = current_cart)
        
    
    def __len__(self):
        return len(self.cart)
    
    
    def get_products(self):
        product_ids = self.cart.keys()
        
        prosucts = Product.objects.filter(id__in = product_ids)
        
        return prosucts
    
    def get_quantities(self):
        return self.cart
    
    
    def get_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in = product_ids)
        
        total = 0
        
        for key,value in self.cart.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += product.sale_price * int(value)
                    else:
                        total += product.price * int(value)
        
        return total
    
    
    def update(self,product,quantity):
        product_id = str(product.id) 
        
        if product_id in self.cart:
            self.cart[product_id] = int(quantity)
            
        self.session.modified = True
        
        if self.request.user.is_authenticated:
            user_profile = Profile.objects.filter(user__id = self.request.user.id)
            
            current_cart = str(self.cart)
            current_cart = current_cart.replace("\'","\"")
            
            user_profile.update(old_cart = current_cart)
    
    def delete(self,product):
        product_id = str(product.id)
        
        if product_id in self.cart:
            del self.cart[product_id]
            
        self.session.modified = True 
        
        if self.request.user.is_authenticated:
            user_profile = Profile.objects.filter(user__id = self.request.user.id)
            
            current_cart = str(self.cart)
            current_cart = current_cart.replace("\'","\"")
            
            user_profile.update(old_cart = current_cart)
    
    def clear(self):
        self.cart.clear()
        self.session.modified = True
        
        if self.request.user.is_authenticated:
            user_profile = Profile.objects.filter(user__id = self.request.user.id)
            
            user_profile.update(old_cart = "")
                        