from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("about-us/", views.about, name="about"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),  
]
