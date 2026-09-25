from django import forms
from django.contrib.auth.forms import AuthenticationForm

from accounts.models import mobile_validator


class MobileNumberForm(forms.Form):
    mobile = forms.CharField(
        label="شماره موبایل",
        max_length=11,
        validators=[mobile_validator],
        widget=forms.TextInput(
            attrs={
                "class": "mobile-input",
                "placeholder": "۰۹xxxxxxxxx",
                "autofocus": True,
                "inputmode": "numeric",
                "dir": "ltr",
            }
        ),
        error_messages={
            "required": "لطفاً شماره موبایل خود را وارد کنید.",
            "max_length": "شماره موبایل نباید بیشتر از ۱۱ رقم باشد.",
        },
    )


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        label="شماره موبایل",
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "۰۹xxxxxxxxx",
                "autofocus": True,
                "inputmode": "numeric",
                "dir": "ltr",
            }
        ),
    )
    password = forms.CharField(
        label="رمز عبور",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "placeholder": "رمز عبور",
            }
        ),
    )

    error_messages = {
        "invalid_login": "شماره موبایل یا رمز عبور اشتباه است.",
        "inactive": "این حساب کاربری غیرفعال است.",
    }
