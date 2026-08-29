from django.urls import path 
from authcart import views 

urlpatterns = [
    path('Signup/', views.signup, name='signup'),
    path('Login/', views.handlelogin, name='handlelogin'),
    path('LogOut/', views.handlelogout, name='handlelogout'),
    

]