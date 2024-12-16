from rest_framework import serializers
from lms.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons(self, obj):
        return LessonSerializer(obj.lessons.all(), many=True).data


class CourseDetailSerializer(serializers.ModelSerializer):
    count_course_with_same_course = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'preview', 'count_course_with_same_course', 'lessons')

    def get_count_course_with_same_course(self, course):
        return Course.objects.filter(lessons__in=course.lessons.all()).distinct().count()

    def get_lessons(self, obj):
        return LessonSerializer(obj.lessons.all(), many=True).data
