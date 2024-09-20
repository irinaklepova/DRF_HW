from django.core.management import BaseCommand

from lms.models import Course, Lesson
from users.models import User, Payment


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Заполнение модели платежа"""

        payment_list = [
            {
                'user': User.objects.get(pk=6),
                'payment_day': '2024-01-01',
                'course_pay': Course.objects.get(pk=11),
                'lesson_pay': None,
                'amount': 150,
                'method': 'cash',
            },
            {
                'user': User.objects.get(pk=7),
                'payment_day': '2024-10-01',
                'course_pay': Course.objects.get(pk=11),
                'lesson_pay': Lesson.objects.get(pk=2),
                'amount': 30,
                'method': 'card'
            },
            {
                'user': User.objects.get(pk=8),
                'payment_day': '2024-09-12',
                'course_pay': Course.objects.get(pk=13),
                'lesson_pay': Lesson.objects.get(pk=5),
                'amount': 50,
                'method': 'card'
            },
        ]
        payment_for_create = []
        for payment_item in payment_list:
            payment_for_create.append(Payment(**payment_item))
        Payment.objects.bulk_create(payment_for_create)
