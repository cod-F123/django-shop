from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
import random
from datetime import datetime , timedelta

# Create your models here.

class AddressUser(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    
    address_title = models.CharField(max_length=50)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=15)
    
    def __str__(self):
        return self.user.username
    

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    old_cart = models.CharField(max_length=250,null=True,blank=True)
    image = models.ImageField(upload_to="upload/images/user",default="upload/images/default/user.png")


def create_profile(sender, instance, created,**kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender = User)

class UserOtp(models.Model):
    email = models.EmailField(max_length=255)
    otp = models.CharField(max_length=5,blank=True, null= True)
    
    date_created = models.DateTimeField(auto_now_add=True)
    date_deleted = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.otp = str(random.randint(10000, 99999))
            self.date_deleted = datetime.now() + timedelta(minutes=2)
        super().save(*args, **kwargs) 
        
               
    def __str__(self):
        return f"{self.otp} -> {self.email}"