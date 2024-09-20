from django.core.management import BaseCommand

from lms.models import Course, Lesson


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Заполнение модели урока"""

        lesson_list = [
            {
                'name_les': 'Как создавать списки',
                'description_les': 'работа с циклами',
                'preview_les': None,
                'video_link': None,
                'course': Course.objects.get(pk=11),
            },
            {
                'name_les': 'Работа со списками',
                'description_les': 'методы списков',
                'preview_les': None,
                'video_link': None,
                'course': Course.objects.get(pk=11),
            },
            {
                'name_les': 'FBV и CBV',
                'description_les': 'спсобы описания контроллеров по FBV и CBV',
                'preview_les': None,
                'video_link': None,
                'course': Course.objects.get(pk=12),
            },
            {
                'name_les': 'Работа с js',
                'description_les': 'способы описания чего-нибудь',
                'preview_les': None,
                'video_link': None,
                'course': Course.objects.get(pk=13),
            }
        ]
        lesson_for_create = []
        for lesson_item in lesson_list:
            lesson_for_create.append(Lesson(**lesson_item))
        Lesson.objects.bulk_create(lesson_for_create)
