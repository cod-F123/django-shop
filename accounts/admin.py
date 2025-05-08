from django.contrib import admin
from .models import AddressUser , Profile

# Register your models here.

@admin.register(AddressUser)
class AddressUserAdmin(admin.ModelAdmin):
    list_display = ["address_title","user"]
    search_fields = ["user__username","state","city"]
    
    
@admin.register(Profile)
class ProfileUserAdmin(admin.ModelAdmin):
    list_display = ["user__username",]
    