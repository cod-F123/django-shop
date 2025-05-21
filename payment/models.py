from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from shop.models import Product
from accounts.models import AddressUser
from django.dispatch import receiver
from django.utils import timezone
from paypal.standard.ipn.models import PayPalIPN

# Create your models here.

class Order(models.Model):
    STATUS_ORDER = (
        ("pending","PEDING"),
        ("processing","PROCESSING"),
        ("cancelled","CANCELLED"),
        ("delivered","DELIVERED")
    )
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    address = models.ForeignKey(AddressUser,on_delete=models.CASCADE)
    
    shiped_date = models.DateTimeField(blank=True,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    date_payed = models.DateTimeField(blank=True,null=True)
    invoice = models.CharField(max_length=255,blank=True,null=True)
    payer_id = models.CharField(max_length=255,blank=True,null=True)
    
    order_status = models.CharField(choices=STATUS_ORDER,default="pending")
    
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    
    def __str__(self):
        return f"{self.user} - {self.id}"
    
    
@receiver(pre_save,sender=Order)
def set_time(sender, instance, **kwargs):
    if instance.pk :
        now = timezone.now()
        obj = sender._default_manager.get(pk=instance.pk)
        if (instance.order_status == "processing") and not (obj.order_status == "processing"):
            instance.date_payed = now
             
        
        elif (instance.order_status == "delivered") and not (obj.order_status == "delivered"):
            instance.shiped_date = now 
            
            


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    product_price = models.IntegerField(default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"order-{self.order.id} orderItem-{self.id}"

@receiver(pre_save,sender = OrderItem)
def set_price(sender, instance, **kwargs):
    if instance.pk: 
        product = instance.product
        # obj = sender._default_manager.get(pk=instance.pk)
        if instance.quantity != 0:
            if product.is_sale:
                instance.product_price = product.sale_price * instance.quantity
            else:
                instance.product_price = product.price * instance.quantity