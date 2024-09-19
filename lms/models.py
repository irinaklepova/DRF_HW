from django.db import models
from config.settings import NULLABLE


class Course(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    preview = models.ImageField(upload_to='lms/', **NULLABLE, verbose_name='Превью')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

