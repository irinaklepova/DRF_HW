from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import NULLABLE
from lms.models import Course, Lesson


class User(AbstractUser):
    """Модель Пользователь"""
    username = None
    email = models.EmailField(unique=True, verbose_name='email')
    phone = models.CharField(max_length=35, **NULLABLE, verbose_name='Телефон')
    city = models.CharField(max_length=100, **NULLABLE, verbose_name='Город')
    avatar = models.ImageField(upload_to='users/', **NULLABLE, verbose_name='Аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    """Модель Платеж"""
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'наличные'),
        ('card', 'перевод на счет'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_day = models.DateField(**NULLABLE, verbose_name='Дата оплаты')
    course_pay = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Оплаченный курс')
    lesson_pay = models.ForeignKey(Lesson, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Оплаченный урок')
    payment_amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=25, choices=PAYMENT_METHOD_CHOICES, **NULLABLE,
                                      verbose_name='Способ оплаты')

    def __str__(self):
        return (f'{self.user}: {self.payment_day}, {self.payment_amount}, '
                f'{self.course_pay if self.course_pay else self.lesson_pay}')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
