from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from .managers import UserManager

# regex
mobile_validator = RegexValidator(
    regex=r"^09\d{9}$",
    message="شماره موبایل باید ۱۱ رقم و با ۰۹ شروع شود. مثال: 09123456789",
)


class User(AbstractUser):
    email = models.EmailField(
        verbose_name="ایمیل",
        unique=True,
    )
    mobile = models.CharField(
        verbose_name="شماره موبایل",
        max_length=11,
        unique=True,
        validators=[mobile_validator],
    )

    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = ["email"]
    
    objects = UserManager()

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.mobile


class Address(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="کاربر",
        on_delete=models.CASCADE,
        related_name="address",
    )
    receiver_name = models.CharField(verbose_name="نام گیرنده", max_length=150)
    receiver_phone = models.CharField(
        verbose_name="شماره تماس گیرنده",
        max_length=11,
        validators=[mobile_validator],
    )
    province = models.CharField(verbose_name="استان", max_length=100)
    city = models.CharField(verbose_name="شهر", max_length=100)
    full_address = models.TextField(verbose_name="آدرس کامل")
    postal_code = models.CharField(verbose_name="کد پستی", max_length=10)

    class Meta:
        verbose_name = "آدرس"

    def __str__(self):
        return f"{self.receiver_name} - {self.city} - {self.full_address}"