from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, mobile, email, password=None, **extra_fields):
        if not mobile:
            raise ValueError("Mobile is required")

        user = self.model(
            mobile=mobile,
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, mobile, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(
            mobile=mobile,
            email=email,
            password=password,
            **extra_fields
        )