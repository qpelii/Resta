from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect, render

from .forms import LoginForm, MobileNumberForm

User = get_user_model()


def mobile_entry(request):
    form = MobileNumberForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        mobile = form.cleaned_data["mobile"]
        request.session["pending_mobile"] = mobile
        
        if User.objects.filter(mobile=mobile).exists():
            return redirect("accounts:login_password")
        return redirect("accounts:register")

    context = {
        "form": form,
        "next": request.GET.get("next", ""),#TODO
    }
    return render(request, "accounts/login.html", context)


def login_password(request):
    mobile = request.session.get("pending_mobile")
    if not mobile:
        return redirect("accounts:login")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            del request.session["pending_mobile"]
            next_url = request.POST.get("next") or "shop:home"
            return redirect(next_url)
    else:
        form = LoginForm(request, initial={"username": mobile})

    context = {
        "form": form,
        "mobile": mobile,
    }
    return render(request, "accounts/login_password.html", context)


def register(request):
    mobile = request.session.get("pending_mobile")
    if not mobile:
        return redirect("accounts:login")

    return render(request, "accounts/register_placeholder.html", {"mobile": mobile})

def AccountLogoutView(request):
    next_page = "shop:home"
    return redirect(next_page)
