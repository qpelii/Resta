from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.mobile_entry, name="login"),
    path("login/password/", views.login_password, name="login_password"),
    path("register/", views.register, name="register"),
]
