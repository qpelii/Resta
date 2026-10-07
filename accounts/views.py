from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth import logout

from .forms import LoginForm, MobileNumberForm

User = get_user_model()


def mobile_entry(request):
    form = MobileNumberForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        mobile = form.cleaned_data["mobile"]
        request.session["pending_mobile"] = mobile
        request.session["pending_next"] = request.POST.get("next", "")
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
            next_url = request.POST.get("next") or ""
            if not url_has_allowed_host_and_scheme(
                next_url, allowed_hosts={request.get_host()},
                require_https=request.is_secure()
            ):
                next_url = None
            return redirect(next_url or "shop:home")
    else:
        form = LoginForm(request, initial={"username": mobile})

    context = {
        "form": form,
        "mobile": mobile,
        "next": request.session.get("pending_next", ""),
    }
    return render(request, "accounts/login_password.html", context)


def register(request):
    mobile = request.session.get("pending_mobile")
    if not mobile:
        return redirect("accounts:login")

    return render(request, "accounts/register_placeholder.html", {"mobile": mobile})

def logout_view(request):
    logout(request)
    return redirect("shop:home")
