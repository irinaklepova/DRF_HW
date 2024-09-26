from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_message(email):
    send_mail(
        'Обновление курса',
        'Обновился курс, на который Вы подписаны',
        settings.EMAIL_HOST_USER,
        email,
    )
