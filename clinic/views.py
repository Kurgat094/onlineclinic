from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User ,Group
from django.contrib.auth.tokens import default_token_generator as token_generator
from .forms import CreateUser,OtpForm,UploadForm
from django.utils import encoding
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from .models import Otp,Upload
from django.contrib import messages
import random,logging
from django.utils import timezone
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from datetime import timedelta
from django.shortcuts import get_object_or_404
from .cart import Cart


# Create your views here.
def signin(request):
    if request.method=="POST":
       form= AuthenticationForm(request,data=request.POST)
       if form.is_valid():
           username=form.cleaned_data.get('username')
           password=form.cleaned_data.get('password')
           user=authenticate(username=username,password=password)
           if user is not None:
                is_verified=Otp.objects.filter(is_verified=1)
                if is_verified:
                    login(request,user)
                    messages.success(request,f"You have loged in successfully")
                    return render(request,'home.html')
                else:
                    messages.error(request,"please verify you accont")
                    return redirect('otp')
    else :
        form=AuthenticationForm()
    return render(request,'signin.html',{'form' :form})

logger = logging.getLogger(__name__)

def signup(request):
    form=CreateUser
    if request.method=='POST':
        form=CreateUser(request.POST)
        if form.is_valid():
            user=form.save()
            name=form.cleaned_data.get('username')
            group=Group.objects.get(name='users')
            user.groups.add(group)
            otp=random.randint(000000,999999)
            # is_user,created=Otp.objects.get_or_create(user=name)
            # is_user.user=name
            # is_user.otp=otp
            Otp.objects.create(user=user,otp=otp)
            # Send the email
            subject = "Successful Login Notification"
            message = f"""Hello,\n\nYou have successfully logged in to your account.
                         'Your Otp is ',
                         'Otp is :{otp},"""
            from_email = "tobiaskipkogei@gmail.com"  
            recipient_list = [user.email]
            try:
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                logger.error(f"Error sending email: {e}")
            return redirect('otp')
    context={
        "form":form
    }
    return render(request,'signup.html',context)

def otp(request):
    if request.method=="POST":
        user_otp=request.POST['otp']
        otp=Otp.objects.filter(otp=user_otp)
        if otp:
           is_verified=1
           verify,created=Otp.objects.get_or_create(otp=user_otp)
           verify.is_verified=int(is_verified)
           verify.save()
           return redirect('signin')
        else:
            return render(request,'otp.html')
    return render(request,'otp.html')

def forgotpassword(request):
    if  request.method == 'POST':
        email=request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request,"User does not exist")
            return redirect('forgotpassword')
            
        
        token=token_generator.make_token(user)
        # uid=urlsafe_base64_decode(force_bytes(user.pk))
        base64_encoded_id =urlsafe_base64_encode(encoding.force_bytes(user.pk))
        
        current_site=get_current_site(request)
        
        resetlink=reverse('resetpassword',kwargs={'uidb64':base64_encoded_id , 'token': token})
        reset_url = f"http://{current_site.domain}{resetlink}"
        # Store the time the link was created
        expiration_time = timezone.now() + timedelta(minutes=4)
        # You may choose to save this in the session or a temporary store
        request.session['reset_link_expiration'] = expiration_time.isoformat()
        
        # email setup
        subject = "Successful Login Notification"
        message = f"""Hello,\n\nYou have requested a reset link
                         'Your this is the reset link ',
                         'Reset password link :{reset_url},"""
        from_email = "tobiaskipkogei@gmail.com"  
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)
        return HttpResponse(f"""
                    <p>A password reset link has been sent to your email.</p>
                    <p>Here is the link as well: <a href="{reset_url}">{reset_url}</a></p>
                """)

        
    return render(request,'forgotpassword.html')
def resetpassword(request, uidb64, token):
    # Check if the reset link has expired
    expiration_time = request.session.get('reset_link_expiration')
    if expiration_time:
        if timezone.now() > timezone.datetime.fromisoformat(expiration_time):
            messages.error(request, "The reset link has expired. Please request a new one.")
            return redirect('forgotpassword')

    try:
        uid = urlsafe_base64_decode(uidb64).decode()  # Decode the user ID
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        if request.method == 'POST':
            newpassword = request.POST.get('newpassword')
            confirmpassword = request.POST.get('confirmpassword')

            if newpassword == confirmpassword:
                # Set and save the new password
                user.set_password(newpassword)
                user.save()
                messages.success(request, "Your password has been reset successfully.")
                return redirect('signin')
            else:
                messages.error(request, "Passwords do not match. Please try again.")
                return redirect('resetpassword', uidb64=uidb64, token=token)

        return render(request, 'resetpassword.html')
    else:
        messages.error(request, "The reset link is invalid or has expired.")
        return redirect('forgotpassword')
    
def signout(request):
    logout(request)
    return redirect('signin')

def home(request):
    return render(request,"home.html")


def upload(request):
    form=UploadForm
    if request.method=="POST":
        form=UploadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('medicines')
    return render(request,"upload_medicine.html",{'form': form})

def medicines(request):
    medicines=Upload.objects.all()
    print(medicines)
    return render(request,"medicines.html",{'medicines':medicines})

# Cart view to display items in the cart
def cart(request):
    cart = request.session.get('cart', {})  # Get cart from session (default to empty dict)
    cart_items = []
    total_price = 0

    for medicine_id, quantity in cart.items():
        medicine_price=1
        medicine = get_object_or_404(Upload, id=medicine_id)
        total_price += medicine_price * quantity
        cart_items.append({
            'medicine': medicine,
            'quantity': quantity,
            'total_price': medicine_price * quantity
        })
    
    return render(request, "cart.html", {'cart_items': cart_items, 'total_price': total_price})

# Function to add an item to the cart
def add_to_cart(request, medicine_id):
    cart = request.session.get('cart', {})

    if str(medicine_id) in cart:
        cart[str(medicine_id)] += 1  # Increase quantity if already in cart
    else:
        cart[str(medicine_id)] = 1  # Add new item with quantity 1
    
    request.session['cart'] = cart  # Update session with cart
    return redirect('cart')  # Redirect to the cart page

def cart_add(self, cart):
    cart=Cart(request.POST)

def admin(request):
    
    return render(request,"admin.html")