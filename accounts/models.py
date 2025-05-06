from django.db import models
from django.contrib.auth.models import User 

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