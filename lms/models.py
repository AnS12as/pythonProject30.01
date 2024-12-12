from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="name of the course", help_text="Choose a course"
    )
    preview = models.ImageField(upload_to="course_previews/", blank=True, null=True)
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="name of the course",
        help_text="Choose a course",
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

    class Meta:
        verbose_name = "lesson"
        verbose_name_plural = "lessons"
