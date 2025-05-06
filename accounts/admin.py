from django.contrib import admin
from .models import AddressUser

# Register your models here.

@admin.register(AddressUser)
class AddressUserAdmin(admin.ModelAdmin):
    list_display = ["address_title","user"]
    search_fields = ["user__username","state","city"]