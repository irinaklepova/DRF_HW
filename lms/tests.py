from rest_framework.test import APITestCase
from django.urls import reverse
from lms.models import Course, Lesson, Subscription
from users.models import User
from rest_framework import status
from django.contrib.auth.models import Group


class LessonTestCase(APITestCase):
    """Тест для модели урока"""

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru')
        self.course = Course.objects.create(name='Test course', owner=self.user)
        self.lesson = Lesson.objects.create(name_les='Test lesson', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Тест вывода одного урока"""
        url = reverse('lms:lesson_get', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['name_les'], self.lesson.name_les)
        self.assertEqual(data['description_les'], self.lesson.description_les)

    def test_lesson_create(self):
        """Тест создания урока"""
        url = reverse('lms:lesson_create')
        data = {'name_les': 'Test lesson 2'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        """Тест изменения урока"""
        url = reverse('lms:lesson_update', args=(self.lesson.pk,))
        data = {'name_les': 'Test lesson NEW'}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name_les'), 'Test lesson NEW')

    def test_lesson_bad_video_url(self):
        """Тест добавления в урок запрещенной ссылки"""
        url = reverse('lms:lesson_update', args=(self.lesson.pk,))
        data = {'video_link': 'http://vk.com'}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data, {'non_field_errors': ['Недопустимый URL-адрес']})

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


class LessonModeratorTestCase(APITestCase):
    """Тест для модели урока с пользователем модератор"""

    def setUp(self):
        self.user = User.objects.create(email='moderator@test.ru', is_staff=True)
        self.my_group = Group.objects.create(name='moderator')
        self.user.groups.add(self.my_group)
        self.lesson = Lesson.objects.create(name_les='Test lesson')
        self.client.force_authenticate(user=self.user)

    def test_lesson_create_moderator(self):
        """Тест создания урока модератором"""
        url = reverse('lms:lesson_create')
        data = {'name_les': 'Test lesson 2'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.all().count(), 1)

    def test_lesson_delete_moderator(self):
        """Тест удаления урока модератором"""
        url = reverse('lms:lesson_delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.all().count(), 1)


class SubscriptionTestCase(APITestCase):
    """Тест для модели подписки"""

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru')
        self.course = Course.objects.create(name='Test сourse', owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscription(self):
        """Тест добавления и удаления подписки на курс"""
        url = reverse('lms:subscription')
        data = {'course': self.course.pk}

        response1 = self.client.post(url, data)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.json(), {'message': 'Подписка добавлена'})
        self.assertEqual(Subscription.objects.all().count(), 1)

        response2 = self.client.post(url, data)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.json(), {'message': 'Подписка удалена'})
        self.assertEqual(Subscription.objects.all().count(), 0)


class CourseTestCase(APITestCase):
    """Тест для модели курса"""

    def setUp(self):
        self.user = User.objects.create(email='test@test.ru')
        self.course = Course.objects.create(name='Test course', owner=self.user)
        self.lesson = Lesson.objects.create(name_les='Test lesson', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        """Тест вывода одного курса"""
        url = reverse('lms:courses-detail', args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['name'], self.course.name)
        self.assertEqual(data['description'], self.course.description)

    def test_course_create(self):
        """Тест создания курса"""
        url = reverse('lms:courses-list')
        data = {'name': 'Test course 2'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        """Тест изменения курса"""
        url = reverse('lms:courses-detail', args=(self.course.pk,))
        data = {'name': 'Test course NEW'}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), 'Test course NEW')

    def test_course_delete(self):
        """Тест удаления курса"""
        self.client.force_authenticate(user=self.user)
        url = reverse('lms:courses-detail', args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        """Тест вывода списка курсов"""
        url = reverse('lms:courses-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "name": self.course.name,
                    "description": self.course.description,
                    "preview": None,
                    "lessons_count": 1,
                    "lessons": [
                        {
                            "id": self.lesson.pk,
                            "name_les": self.lesson.name_les,
                            "description_les": self.lesson.description_les,
                            "preview_les": None,
                            "video_link": None,
                            "course": self.course.pk,
                            "owner": self.user.pk
                        },
                    ],
                    "is_subscribed": False
                }
            ]
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
