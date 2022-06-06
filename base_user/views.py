from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.core.mail import send_mail
from uuid import uuid4
from django.contrib import messages
from django.contrib.auth import get_user_model, login,authenticate,logout
from django.conf import settings
User = get_user_model()

def loginUser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(email=email).first()
        if user_obj is None:
            messages.error(request,"User not found")
            return redirect('login')
        user = authenticate(email=email,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.error(request,"Password is incorrect")
            return redirect('login')
    return render(request,'login.html')

def register(request):   
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user =form.save(commit=False)
            user.token = uuid4()
            user.is_active = False
            email=user.email
            form.save()
            send_confirmation_email(request,email)
            return redirect('login')
    context = {
        'form':form
    }   
    return render(request,'register.html',context)


def verify(request,token):
    user = User.objects.filter(token=token).first()
    user.is_active = True
    user.save()
    context = {
        'email':user.email,
    }
    return render(request,'verify.html',context)

def send_confirmation_email(request,email):
    user = User.objects.filter(email=email).first()
    host = request.META['HTTP_HOST']
    subject = "Confirmation Email by Qsmart"
    message = f"Please click this link and verify your account {host}/user/verify/{user.token}/"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def logoutUser(request):
    logout(request)
    return redirect('login')