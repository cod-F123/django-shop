from django import forms 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserChangeForm

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User 
        fields = ["username","last_name","first_name","email"]