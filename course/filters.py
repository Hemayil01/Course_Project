from django_filters import rest_framework as filters
from .models import Course, Lesson, Enrollment, Progress
from django.utils import timezone



class CourseFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    instructor_name = filters.CharFilter(field_name='instructor__username', lookup_expr='icontains')
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')
    duration_min = filters.NumberFilter(field_name='duration_days', lookup_expr='gte')
    duration_max = filters.NumberFilter(field_name='duration_days', lookup_expr='lte')

    class Meta:
        model = Course
        fields = ['title', 'instructor_name', 'price_min', 'price_max', 'duration_min', 'duration_max']


class LessonFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    course_id = filters.NumberFilter(field_name='course__id')

    class Meta:
        model = Lesson
        fields = ['title', 'course_id']


class EnrollmentFilter(filters.FilterSet):
    student_id = filters.NumberFilter(field_name='student__id')
    course_title = filters.CharFilter(field_name='course__title', lookup_expr='icontains')
    active_only = filters.BooleanFilter(method='filter_active')

    class Meta:
        model = Enrollment
        fields = ['student_id', 'course_title']

    def filter_active(self, queryset, name, value):
        if value:
            now = timezone.now()
            return queryset.filter(status='active', end_date__gt=now)
        return queryset


class ProgressFilter(filters.FilterSet):
    student_id = filters.NumberFilter(field_name='student__id')
    course_id = filters.NumberFilter(field_name='course__id')
    completed_only = filters.BooleanFilter(method='filter_completed')

    class Meta:
        model = Progress
        fields = ['student_id', 'course_id']

    def filter_completed(self, queryset, name, value):
        if value:
            return queryset.filter(completed_lessons__gt=0)
        return queryset