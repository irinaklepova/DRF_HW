from rest_framework import serializers

from lms.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для уроков"""

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курсов"""
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson', many=True, read_only=True)

    def get_lessons_count(self, obj):
        return obj.lesson.count()

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'preview', 'lessons_count', 'lessons']
