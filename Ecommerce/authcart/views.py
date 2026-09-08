from django.shortcuts import render, redirect ,HttpResponse

from django.contrib.auth.models import User

def signup(request):
       if request.method=='POST':
            email=request.POST['email']
            password=request.POST['pass1']
            confirm_password=request.POST['pass2']
            if password!=confirm_password:
                return HttpResponse("Password and confirm password are not same! Please try again")
                # return render (request, "authentication/signup.html")

            try: 
                 if User.objects.get(username=email):
                      return HttpResponse("Email is already registered! Please try again")
                    # return render (request, 'authentication/signup.html')
            
               
            except Exception as identifier:
                 pass 
            user= User.objects.create_user(email,email,password)
            user.save()
            return HttpResponse("Your account has been successfully created! Please login to continue")
            
       return render (request, "authentication/signup.html")


def handlelogin(request): 
    return render (request, "authentication/login.html")

def handlelogout(request):
    return redirect ('/auth/login')
    