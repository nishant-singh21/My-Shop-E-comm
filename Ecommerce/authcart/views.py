from django.shortcuts import render, redirect ,HttpResponse

from django.contrib.auth.models import User
from django.contrib import messages


def signup(request):
       if request.method=='POST':
            email=request.POST['email']
            password=request.POST['pass1']
            confirm_password=request.POST['pass2']
            if password!=confirm_password:
                messages.warning(request, "Passwords do not match!")
                return render (request, "signup.html")

            try: 
                 if User.objects.get(username=email):
                      messages.error(request, "Email is already registered! Please try again")
                      return render (request, "signup.html")
                    # return render (request, 'authentication/signup.html')
            
               
            except Exception as identifier:
                 pass 
            user= User.objects.create_user(email,email,password)
            user.save()
            messages.success(request, "Your account has been successfully created! Please login to continue")
            return redirect('auth/login')

       return render (request, "signup.html")


def handlelogin(request): 
    return render (request, "login.html")

def handlelogout(request):
    return redirect ('/login')
    