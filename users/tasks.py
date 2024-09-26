from datetime import timedelta

from celery import shared_task
from django.utils import timezone
from users.models import User


@shared_task
def block_user():
    now = timezone.now()
    users = User.objects.filter(last_login__lte=now - timedelta(days=30), is_active=True)
    for user in users:
        user.is_active = False
        user.save()
