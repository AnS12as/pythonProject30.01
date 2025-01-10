from django.http import JsonResponse
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Course, Subscription, Payment

from users.permissions import IsModerator, IsOwner
from .models import Course, Lesson
from .paginators import StandardResultsPagination
from .serializer import CourseSerializer, LessonSerializer, CourseDetailSerializer
from .services import create_stripe_checkout_session, create_stripe_price, create_stripe_product
from .tasks import send_course_update_email


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="description from swagger_auto_schema via method_decorator"
))
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsOwner()]
        elif self.action in ['create', 'destroy']:
            return [IsAuthenticated(), IsModerator()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer


class LessonListCreateAPIView(ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = StandardResultsPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "Subscription removed"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Subscription added"

        return Response({"message": message})


class CreatePaymentView(APIView):
    def post(self, request):
        data = request.data
        product_name = data.get("product_name")
        product_description = data.get("product_description", "")
        product_price = data.get("product_price")

        if not product_name or not product_price:
            return Response({"error": "Product name and price are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:

            product = create_stripe_product(product_name, product_description)

            price = create_stripe_price(product["id"], product_price)

            success_url = "http://127.0.0.1:8000/success/"
            cancel_url = "http://127.0.0.1:8000/cancel/"
            session = create_stripe_checkout_session(price["id"], success_url, cancel_url)

            payment = Payment.objects.create(
                product_name=product_name,
                product_description=product_description,
                product_price=product_price,
                stripe_product_id=product["id"],
                stripe_price_id=price["id"],
                stripe_session_id=session["id"],
                payment_url=session["url"],
            )

            return Response({"payment_url": session["url"]}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def update_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    course.materials_updated = True
    course.save()

    subscribers = Subscription.objects.filter(course=course).values_list('user__email', flat=True)

    subject = f"Обновление материала курса: {course.title}"
    message = f"Материалы курса '{course.title}' были обновлены. Проверьте их на сайте."

    send_course_update_email.delay(subject, message, list(subscribers))

    return JsonResponse({'status': 'success', 'message': 'Курс обновлен, пользователи уведомлены.'})
