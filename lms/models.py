from django.db import models
from config.settings import NULLABLE


class Course(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    preview = models.ImageField(upload_to='lms/', **NULLABLE, verbose_name='Превью')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    name_les = models.CharField(max_length=200, verbose_name='Название урока')
    description_les = models.TextField(**NULLABLE, verbose_name='Описание урока')
    preview_les = models.ImageField(upload_to='lms/', **NULLABLE, verbose_name='Превью урока')
    video_link = models.URLField(max_length=200, **NULLABLE, verbose_name='Ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Курс')

    def __str__(self):
        return f'{self.name_les}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
