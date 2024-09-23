from rest_framework.test import APITestCase
from django.urls import reverse
from lms.models import Course, Lesson
from users.models import User
from rest_framework import status


class LessonTestCase(APITestCase):
    """Тест для модели урока"""

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru')
        self.course = Course.objects.create(name='Test course', owner=self.user)
        self.lesson = Lesson.objects.create(name_les='Test lesson', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Тест вывода одного курса"""
        url = reverse('lms:lesson_get', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['name_les'], self.lesson.name_les)
        self.assertEqual(data['description_les'], self.lesson.description_les)

    def test_lesson_create(self):
        """Тест создания урока"""
        url = reverse('lms:lesson_create')
        data = {'name_les': 'Test Lesson 2'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        """Тест изменения урока"""
        url = reverse('lms:lesson_update', args=(self.lesson.pk,))
        data = {'name_les': 'Test Lesson NEW'}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name_les'), 'Test Lesson NEW')

    def test_lesson_list(self):
        """Тест вывода списка уроков"""
        url = reverse('lms:lesson_list')
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name_les": self.lesson.name_les,
                    "description_les": self.lesson.description_les,
                    "preview_les": None,
                    "video_link": None,
                    "course": self.course.pk,
                    "owner": self.user.pk
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_lesson_delete(self):
        """Тест удаления урока"""
        self.client.force_authenticate(user=self.user)
        url = reverse('lms:lesson_delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)
