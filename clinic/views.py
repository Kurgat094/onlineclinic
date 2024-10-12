from django.shortcuts import render

# Create your views here.
def signin(requets):
    return render(requets,"signin.html")

def signup(requets):
    return render(requets,"signup.html")
def home(requets):
    return render(requets,"home.html")