from rest_framework import serializers
from lms.models import Course, Lesson, Subscription
from lms.validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_youtube_url])

    class Meta:
        model = Lesson
        fields = ['id', 'course', 'name', 'description', 'video_url', 'preview']


class CourseSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'owner']

    def get_lessons(self, obj):
        return LessonSerializer(obj.lessons.all(), many=True).data

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False


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


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
