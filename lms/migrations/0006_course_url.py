# Generated by Django 5.1.1 on 2024-09-22 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0005_course_owner_lesson_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='url',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на курс'),
        ),
    ]
