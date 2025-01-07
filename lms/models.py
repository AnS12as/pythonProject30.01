from django.db import models

from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
        help_text="Provide a description for the course"
    )
    preview = models.ImageField(
        upload_to="course_previews/",
        blank=True,
        null=True,
        verbose_name="Preview"
    )
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="owned_courses",
        verbose_name="Owner",
        help_text="User who created this course",
        default=1
    )

    class Meta:
        verbose_name = "course"
        verbose_name_plural = "courses"


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="description of the lesson",
        help_text="Provide a lesson description",
    )
    preview = models.ImageField(upload_to="lesson_previews/", blank=True, null=True)
    video_url = models.URLField()
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="owned_lessons",
        verbose_name="Owner",
        help_text="User who created this lesson",
        default=1
    )

    class Meta:
        verbose_name = "lesson"
        verbose_name_plural = "lessons"


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    course = models.ForeignKey('lms.Course', on_delete=models.CASCADE, related_name="subscribers")

    class Meta:
        unique_together = ('user', 'course')
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        return f"{self.user.email} subscribed to {self.course.title}"


class Payment(models.Model):
    product_name = models.CharField(max_length=255)
    product_description = models.TextField(null=True, blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_product_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_price_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_session_id = models.CharField(max_length=255, null=True, blank=True)
    payment_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
