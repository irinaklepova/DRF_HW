from rest_framework import serializers

from lms.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курсов"""
    lessons_count = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lesson_set.count()

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'lessons_count', ]


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для уроков"""

    class Meta:
        model = Lesson
        fields = '__all__'
