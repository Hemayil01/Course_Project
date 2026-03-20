from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, status, filters as drf_filters
from django_filters import rest_framework as filters

from .models import Course, Lesson, Enrollment, Progress
from .serializers import (
    CourseModelSerializer,
    CourseListModelSerializer,
    LessonModelSerializer,
    EnrollmentModelSerializer,
    ProgressModelSerializer
)
from .permissions import (
    IsInstructorOrAdmin,
    IsStudentOrAdmin,
    CanManageCourses,
    CanManageLessons,
    CanManageEnrollments,
    CanManageProgress
)
from .paginators import CustomPageNumberPagination
from .filters import CourseFilter, LessonFilter


class HealthCheckAPIView(APIView):
    def get(self, request):
        return Response({'status': 'ok'})

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer
    permission_classes = [permissions.IsAuthenticated, CanManageCourses]
    pagination_class = CustomPageNumberPagination
    filter_backends = [filters.DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    search_fields = ['title', 'instructor__username']
    ordering_fields = ['title', 'price', 'duration_days']
    ordering = ['title']
    filterset_class = CourseFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListModelSerializer
        return CourseModelSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated, IsInstructorOrAdmin]
        return [perm() for perm in permission_classes]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonModelSerializer
    permission_classes = [permissions.IsAuthenticated, CanManageLessons]
    filter_backends = [filters.DjangoFilterBackend, drf_filters.OrderingFilter]
    filterset_class = LessonFilter
    ordering_fields = ['order', 'title']
    ordering = ['order']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated, CanManageLessons]
        return [perm() for perm in permission_classes]


class EnrollmentAPIView(APIView):
    serializer_class = EnrollmentModelSerializer

    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT']:
            permission_classes = [permissions.IsAuthenticated, IsStudentOrAdmin, CanManageEnrollments]
        else:
            permission_classes = [permissions.IsAuthenticated, IsStudentOrAdmin]
        return [perm() for perm in permission_classes]

    def post(self, request, course_id=None):
        serializer = EnrollmentModelSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        enrollment = serializer.save()
        return Response(
            {'message': 'Enrolled successfully', 'enrollment': EnrollmentModelSerializer(enrollment).data},
            status=status.HTTP_201_CREATED
        )

    def get(self, request):
        if request.user.role in ['instructor', 'admin']:
            enrollments = Enrollment.objects.all()
        else:
            enrollments = Enrollment.objects.filter(student=request.user)
        return Response(EnrollmentModelSerializer(enrollments, many=True).data)


class ProgressAPIView(APIView):
    serializer_class = ProgressModelSerializer
    permission_classes = [permissions.IsAuthenticated, CanManageProgress]

    def get(self, request, course_id=None):
        progress = Progress.objects.filter(student=request.user, course_id=course_id).first()
        if not progress:
            return Response({'message': 'No progress found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(ProgressModelSerializer(progress).data)

    def post(self, request, course_id=None):
        progress, created = Progress.objects.get_or_create(student=request.user, course_id=course_id)

        completed_lessons = request.data.get('completed_lessons', progress.completed_lessons)
        total_lessons = progress.course.lessons.count()

        if completed_lessons > total_lessons:
            completed_lessons = total_lessons

        progress.completed_lessons = completed_lessons
        progress.save()

        return Response(ProgressModelSerializer(progress).data, status=status.HTTP_200_OK)