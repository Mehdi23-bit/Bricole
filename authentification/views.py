from django.shortcuts import render,redirect
from .forms import RegistationForm,LoginForm,EmailForm
from django.contrib.auth import  login
from .Email import EmailLogin 
import random
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth import logout
# Create your views here.

#view de signup 
def sign_up(request):
   
    form=RegistationForm()
    if request.method == 'POST':
        form=RegistationForm(request.POST)
        if form.is_valid():
            new_user=form.save(commit=False)
            new_user.username=generate(form.cleaned_data['first_name'],form.cleaned_data['last_name'])
            print(form.cleaned_data['last_name'])
            print(form.cleaned_data['first_name'])
            new_user.save()
            print(new_user.username)
            return redirect("signin")

    return render(request,'signup.html',{'form':form})

@login_required
def home(request):
    return render(request,"home.html")

def generate(first_name,last_name):
        charaters=['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', 
 ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~',
 '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        username=f"{random.choice(charaters)}{last_name}{random.choice(charaters)}{first_name}{random.choice(charaters)}"
        return username

#view de sign in
def sign_in(request):
     import sys
     import os

     sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # add current folder to sys.path

     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Bricole.settings")

     import django
     django.setup()

     from django.conf import settings

     print(settings.ALLOWED_HOSTS)

     if request.user.is_authenticated :
          return redirect('home')
     form=LoginForm()
     if request.method=='POST':
          loginEmail=EmailLogin() 
          email=request.POST["email"]
          password=request.POST["password"]  
          user=loginEmail.authenticate(request,email,password)
          if user is not None:
               login(request,user)
               return redirect("home")
          return render(request,'signin.html',{'eror':'there is a problem'})
     return render(request,'signin.html',{'form':form})



def logout_view(request):
     logout(request)
     return redirect("signin")

def sendEmail(request):
     if request.method=='POST':
          email=request.POST['email']
          send_mail(
     "Subject here",
     "Here is the message.",
     "elmehdiiskandar3@gmail.com",
     [f"{email}"],
     fail_silently=False,
     )
          return render(request,'email_form.html',{'success':'you the email is in your inbox check it'})
     
     return   render(request,'email_form.html')


