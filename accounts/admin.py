from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User, Address

# Register your models here.

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = ("-date_joined",) 
    list_display = ("mobile", "email", "first_name", "last_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("mobile", "email", "first_name", "last_name")
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("اطلاعات رستا", {"fields": ("mobile",)}),
    )
    fieldsets = (
        (None, {"fields": ("mobile", "password")}),
        ("اطلاعات شخصی", {"fields": ("first_name", "last_name", "email")}),
        (
            "دسترسی‌ها",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("تاریخ‌های مهم", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("mobile", "email", "password1", "password2"),
            },
        ),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("receiver_name", "user", "province", "city", "postal_code")
    list_filter = ("province", "city")
    search_fields = ("receiver_name", "receiver_phone", "user__mobile", "user__email")
    raw_id_fields = ("user",)  # جلوگیری از dropdown سنگین اگه کاربرا زیاد بشن
