from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import * 
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

@login_required(login_url="/")
def home(request):
    return render(request,'home.html')

def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        newuser = User.objects.filter(username = username).first()
        if newuser is None:
            messages.success(request, "User not found...")
            return redirect('/login')
        
        newProfile = Profile.objects.filter(user = newuser).first()
        if not newProfile.is_verified:
            messages.success(request, "Profile is not verified...")
            return redirect('/login')
        
        user = authenticate(username = username, password = password)
        
        if user is None:
            messages.success(request, "Wrong password...")
            return redirect("/login")
        
        login(request, user)
        return redirect("/")
          
    return render(request, 'login.html')

def register(request):
    
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            if User.objects.filter(username = username).first():
                messages.success(request, "Username is taken.")
                return redirect('/register')

            if User.objects.filter(email = email).first():
                messages.success(request, "Email is taken.")
                return redirect('/register')
            
            newUser = User(username = username, email = email)
            newUser.set_password(password)
            newUser.save()
            
            auth_token = str(uuid.uuid4())
            newProfile = Profile.objects.create(user = newUser, auth_token = auth_token)
            newProfile.save()
            send_registration_mail(email, auth_token)
            return redirect('/token')
            
        except Exception as e:
            print(e)
        
        
    return render(request, 'register.html')

def success(request):
    return render(request, 'success.html')

def token_send(request):
    return render(request, 'token_send.html')

def send_registration_mail(email, token):
    subject = 'Your account need to be verified'
    message = f'Hi click please the link to verify your account http://localhost:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
      
def verify(request, auth_token):
    try:
        newProfile = Profile.objects.filter(auth_token = auth_token).first()
        if newProfile:
            if newProfile.is_verified:
                messages.success(request, "Your account is already verified.")
                return
            
            newProfile.is_verified = True
            newProfile.save()
            messages.success(request, "Your account has been verified.")
            return redirect("/login")
        
        else:
            return redirect('/error')
        
    except Exception as e:
        print(e)
        
def error_page(request):
    return render(request, 'error.html')