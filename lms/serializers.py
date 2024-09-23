from rest_framework import serializers

from lms.models import Course, Lesson, Subscription
from lms.validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для уроков"""

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [UrlValidator(field='video_link')]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курсов"""
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson', many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = None
        if request:
            user = request.user
        return obj.course_subscription.filter(user=user).exists()

    def get_lessons_count(self, obj):
        return obj.lesson.count()

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'preview', 'lessons_count', 'lessons', 'is_subscribed']
        validators = [UrlValidator(field='url')]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
