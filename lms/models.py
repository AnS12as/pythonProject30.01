from django.db import models


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
