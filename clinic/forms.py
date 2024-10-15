from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import *



class CreateUser(UserCreationForm):
    email=forms.EmailField()
    class Meta:
      model=User
      fields=['username','email', 'password1','password2']
    
        
class OtpForm(forms.ModelForm):
    class Meta:
        model=Otp
        fields=['otp','is_verified']
        
        
class UploadForm(forms.ModelForm):
    class Meta:
        model=Upload
        fields=['medicine_name','medicine_image','medicine_price','medicine_description']