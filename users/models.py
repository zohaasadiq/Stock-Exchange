from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
    Group,
    Permission,
)

class CustomAccountManager(BaseUserManager):
    def create_superuser(self, username, password, balance, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")

        return self.create_user(username, password, balance, **other_fields)

    def create_user(self, username, password, balance, **otherfields):
        if not username:
            raise ValueError(_("You must provide a username!"))

        user = self.model(username=username, balance=balance, **otherfields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    balance = models.FloatField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    groups = models.ManyToManyField(Group, related_name="newuser_set", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="newuser_set", blank=True
    )

    objects = CustomAccountManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["balance"]

    def __str__(self):
        return self.username
