from django.shortcuts import render

# Create your views here.

def blog(request):
    return render(request, "shop/home.html")#TODO: create template for blog page