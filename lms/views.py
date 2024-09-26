from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from lms.tasks import send_message #subscription_message,
from lms.models import Course, Lesson, Subscription
from lms.paginators import CoursePagination, LessonPagination
from users.permissions import IsOwner, IsStaff
from lms.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet для модели курса"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePagination

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (IsAuthenticated, ~IsStaff,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsAuthenticated, IsStaff | IsOwner,)
        elif self.action == 'destroy':
            self.permission_classes = (IsAuthenticated, ~IsStaff | IsOwner,)

        return super().get_permissions()

    def perform_update(self, serializer):
        course = serializer.save()
        subscription = Subscription.objects.filter(course=course)
        if subscription:
            subscription_email = []
            for subscript in subscription:
                subscription_email.append(subscript.user.email)
                print(subscript.user.email)
                print(subscription_email)
            send_message.delay(subscription_email)

        course.save()


class LessonCreateAPIView(generics.CreateAPIView):
    """Generic-класс для создания урока"""
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsStaff,)

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """Generic-класс для просмотра уроков."""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsStaff | IsOwner,)
    pagination_class = LessonPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Generic-класс для просмотра урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsStaff | IsOwner,)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Generic-класс для редактирования урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsStaff | IsOwner,)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Generic-класс для удаления урока"""
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, ~IsStaff | IsOwner,)


class SubscriptionAPIView(APIView):
    """Класс для добавления и удаления подписки на курс"""
    permission_classes = (IsAuthenticated,)
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    @swagger_auto_schema(request_body=SubscriptionSerializer)
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)
        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'
        return Response({'message': message})
