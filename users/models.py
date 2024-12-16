from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
from lms.models import Course, Lesson


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Enter your email address"
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
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Photo",
        help_text="Upload your photo",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'CASH'),
        ('transfer', 'TRANSFER'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'PENDING'),
        ('completed', 'COMPLETED'),
        ('failed', 'FAILED'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='USER'
    )
    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='DATE OF PAYMENT'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='PAID COURSE'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='PAID LESSON'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='AMOUNT OF PAYMENT'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name='TYPE OF PAYMENT'
    )
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        verbose_name='STATUS OF PAYMENT'
    )

    def __str__(self):
        return f'Payment {self.id} by {self.user}'

    def is_course_payment(self):
        return self.course is not None

    def is_lesson_payment(self):
        return self.lesson is not None

    def save(self, *args, **kwargs):
        if not self.course and not self.lesson:
            raise ValueError("Должен быть указан либо курс, либо урок.")
        if self.course and self.lesson:
            raise ValueError("Нельзя указать одновременно курс и урок.")
        super().save(*args, **kwargs)
