from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name="home"),
    path("signin/",signin,name="signin"),
    path("signup/",signup,name="signup"),
    path("otp/",otp,name="otp"),
    path('signout/',signout,name="signout"),
    path('forgotpassword',forgotpassword,name="forgotpassword"),
    path('resetpassword',resetpassword,name="resetpassword"),
    path('resetpassword/<uidb64>/<token>/', resetpassword, name='resetpassword'),
    path('upload/',upload,name="upload"),
    path('medicines/',medicines,name="medicines"),
]
