from django.shortcuts import render


#Main Templates Backend
def home(request):
    return render(request,"Main/home.htm")


#Auth Templates Backend
def signin(request):
    return render(request,"Auth/signin.htm")


#Admin Templates Backend
def addServices(request):
    pass