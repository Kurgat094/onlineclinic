from django.db import models
from django.contrib.auth.models import User
import random,string,datetime
# Create your models here.
    
class Otp(models.Model): 
    user=models.CharField(max_length=10,blank=True,null=True)
    otp=models.CharField(max_length=6)
    is_verified=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)