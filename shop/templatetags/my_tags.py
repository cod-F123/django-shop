from django import template 
from shop.models import WishedProduct

register = template.Library()

@register.filter(name="is_wished")
def is_wished(user,product_id):
    try:
        return WishedProduct.objects.filter(product__id = product_id ,user= user).exists()
    except:
        pass