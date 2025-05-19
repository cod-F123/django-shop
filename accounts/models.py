from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save

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