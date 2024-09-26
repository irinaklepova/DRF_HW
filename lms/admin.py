from django.contrib import admin

from lms.models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'owner')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name_les', 'description_les', 'course', 'owner')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')
