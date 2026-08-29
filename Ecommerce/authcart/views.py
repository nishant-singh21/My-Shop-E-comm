from django.shortcuts import render, redirect 

def signup(request):
    return render (request, "authcaartentication/signup.html")


def handlelogin(request):
    return render (request, "authentication/login.html")

def handlelogout(request):
    return redirect ('/authcart/login')
    