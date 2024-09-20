from django.core.management import BaseCommand

from lms.models import Course, Lesson
from users.models import User, Payment


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Заполнение модели пользователя"""

        user_list = [
            {
                'email': 'test1@mail.ru',
                'phone': None,
                'city': 'Москва',
                'avatar': None,
            },
            {
                'email': 'test2@mail.ru',
                'phone': None,
                'city': 'Саратов',
                'avatar': None,
            },
            {
                'email': 'test3@mail.ru',
                'phone': None,
                'city': 'Самара',
                'avatar': None,
            }
        ]
        users_for_create = []
        for user_item in user_list:
            users_for_create.append(User(**user_item))
        User.objects.bulk_create(users_for_create)
