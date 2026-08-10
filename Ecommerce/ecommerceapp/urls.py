from  django.urls import render 
from ecommerceapp import views 

urlpatterns = [
    path('', views.index, name = "index"),
]
