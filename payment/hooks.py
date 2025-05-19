
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from .models import Order
import time

@receiver(valid_ipn_received)
def paypal_paymetn_received(sender,**kwargs):    
    # Grab the info that paypal send
    paypal_obj = sender
    if paypal_obj.payment_status == 'Completed':
        # Grab the invoice
        my_invoice = str(paypal_obj.invoice)
        
        order = Order.objects.get(invoice = my_invoice)
        
        order.order_status = "processing"
        order.payer_id = str(paypal_obj.payer_id)
        order.save()