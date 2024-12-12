from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Enter your email adress"
    )
    phone = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        verbose_name="Phone",
        help_text="Enter your phone number",
    )
    city = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(
        upload_to="users / avatars/",
        blank=True,
        null=True,
        verbose_name="Photo",
        help_text="Upload your photo",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
