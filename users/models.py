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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', verbose_name='Пользователь')
    payment_day = models.DateField(**NULLABLE, verbose_name='Дата оплаты')
    course_pay = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Оплаченный курс')
    lesson_pay = models.ForeignKey(Lesson, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Оплаченный урок')
    amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    method = models.CharField(max_length=25, choices=PAYMENT_METHOD_CHOICES, **NULLABLE,
                                      verbose_name='Способ оплаты')
    session_id = models.CharField(max_length=255, **NULLABLE, help_text='Укажите ID сессии', verbose_name='ID сессии')
    link = models.URLField(max_length=400, **NULLABLE, help_text='Укажите ссылку на оплату',
                           verbose_name='Ссылка на оплату')

    def __str__(self):
        return (f'{self.user}: {self.payment_day}, {self.amount}, '
                f'{self.course_pay if self.course_pay else self.lesson_pay}')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
