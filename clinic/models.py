from django.db import models
from django.contrib.auth.models import User
import random,string,datetime
# Create your models here.
    
class Otp(models.Model): 
    user=models.CharField(max_length=10,blank=True,null=True)
    otp=models.CharField(max_length=6)
    is_verified=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    
class Upload(models.Model):
    medicine_name=models.CharField(max_length=100)
    medicine_image=models.ImageField(upload_to='static/images/')
    medicine_price=models.FloatField()
    medicine_description=models.TextField()
    
    
    @property
    def image_url(self):
        try:
            url = self.medicine_image.url
        except:
            url = ''
        return url