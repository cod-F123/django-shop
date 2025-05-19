from django import forms
from django.contrib.auth.forms import UserCreationForm , UserChangeForm , PasswordChangeForm
from django.contrib.auth.models import User 
from .models import AddressUser

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","username","email","password1","password2"]


class AddressUserForm(forms.ModelForm):
    class Meta:
        model = AddressUser
        fields = ["address_title","street","city","state","zip_code"]
        
        
class UserProfileChange(UserChangeForm):
    class Meta:
        model = User 
        fields = ["first_name","last_name","username"]
        
class ChangePAsswordUser(PasswordChangeForm):
    class Meta:
        model = User 
        fields = ["old_password","new_password1","new_password2"]