from datetime import timedelta

from celery import shared_task
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
from users.models import User


@shared_task
def sample_task():
    print("This is a Celery task running!")


@shared_task
def send_course_update_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        recipient_list,
        fail_silently=False,
    )


class CustomUser(AbstractUser):
    pass


@shared_task
def deactivate_inactive_users():
    one_month_ago = now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)
    count = inactive_users.update(is_active=False)
    return f"{count} пользователей деактивировано."
