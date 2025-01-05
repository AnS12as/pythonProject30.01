from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Course, Lesson, Subscription
from django.contrib.auth.models import Group

User = get_user_model()


class LessonCourseTests(APITestCase):
    def setUp(self):
        self.api_client = APIClient()
        # Создание пользователей
        self.owner = User.objects.create_user(email="owner@example.com", password="password")
        self.moderator_user = User.objects.create_user(email="moderator@example.com", password="password")
        self.regular_user = User.objects.create_user(email="user@example.com", password="password")

        # Добавляем модератора в группу
        moderator_group, _ = Group.objects.get_or_create(name="Moderators")
        self.moderator_user.groups.add(moderator_group)

        # Создание курса и урока
        self.course = Course.objects.create(title="Test Course", description="Test Description", owner=self.owner)
        self.lesson = Lesson.objects.create(course=self.course, name="Test Lesson", video_url="https://youtube.com/example")

    def test_create_lesson_as_owner(self):
        self.api_client.force_authenticate(user=self.owner)
        data = {
            "course": self.course.id,
            "name": "New Lesson",
            "description": "Test description",
            "video_url": "https://youtube.com/example"
        }
        response = self.api_client.post("/lms/lessons/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_lesson_as_moderator(self):
        self.api_client.force_authenticate(user=self.moderator_user)
        data = {
            "course": self.course.id,
            "name": "Moderator Lesson",
            "video_url": "https://youtube.com/mod_example",
        }
        response = self.api_client.post("/lms/lessons/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_lesson_as_owner(self):
        self.api_client.force_authenticate(user=self.owner)
        data = {"name": "Updated Lesson"}
        response = self.api_client.patch(f"/lms/lessons/{self.lesson.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, "Updated Lesson")

    def test_delete_lesson_as_moderator(self):
        self.api_client.force_authenticate(user=self.moderator_user)
        response = self.api_client.delete(f"/lms/lessons/{self.lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_subscription_add_remove(self):
        self.api_client.force_authenticate(user=self.owner)
        response = self.api_client.post("/lms/subscriptions/", {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Subscription added")

        response = self.api_client.post("/lms/subscriptions/", {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Subscription removed")
