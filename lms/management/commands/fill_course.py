from django.core.management import BaseCommand

from lms.models import Course, Lesson


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Заполнение модели курса"""

        course_list = [
            {
                'name': 'Python для начинающих',
                'description': 'Отличный курс для начинающих',
                'preview': None,
            },
            {
                'name': 'Python для опытных',
                'description': 'Отличный курс для тех, кто хочет расширить свои навыки',
                'preview': None,
            },
            {
                'name': 'Web-разработка',
                'description': 'Курс для тех, кто хочет прокачать навыки работы с css, js',
                'preview': None,
            }
        ]
        course_for_create = []
        for course_item in course_list:
            course_for_create.append(Course(**course_item))
        Course.objects.bulk_create(course_for_create)
