from django.db import models
from django.contrib.auth.models import User
import random

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="upload/images/category/")
    
    description = models.TextField(blank=True,null=True) 
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=255)
    mini_description = models.TextField()
    factory = models.CharField(max_length=255)
    image = models.ImageField(upload_to="upload/images/product")
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    slug = models.SlugField(unique=True,blank=True,null=True)
    
    price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    is_sale = models.BooleanField(default=False)
    
    @property
    def sale_price(self):
        if self.is_sale:
            sale_p = self.price - (self.price * self.discount / 100)
            return sale_p
    
    def save(self,*args,**kwags):
        super().save(*args,*kwags)
        
        if not self.slug:
            random_num = random.randint(10000,99999)
            self.slug = str(self.name) + str(self.factory) + str(random_num)
            self.save()
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="upload/images/product")
    
    def __str__(self):
        return super().__str__()
        
    

class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_detailname = models.CharField(max_length=50)
    product_detail = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.product_detailname} : {self.product_detail}"

class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    feature = models.CharField(max_length=255)
    
    def __str__(self):
        return super().__str__()

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=40)
    comment = models.TextField()
    
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username