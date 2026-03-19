from django.contrib import admin
from .models import Course, Lesson, Enrollment, Progress



@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'price', 'duration_days', 'student_count']
    list_filter = ['duration_days', 'price', 'instructor']
    search_fields = ['title', 'description', 'instructor__username']
    ordering = ['title']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['course', 'title', 'order']
    list_filter = ['course', 'order']
    search_fields = ['title', 'course__title']
    ordering = ['course', 'order']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_at', 'end_date', 'status']
    list_filter = ['status', 'end_date', 'course']
    search_fields = ['student__email', 'course__title']
    ordering = ['-enrolled_at']
    readonly_fields = ['enrolled_at']


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'completed_lessons', 'completion_percentage', 'last_updated']
    list_filter = ['course', 'last_updated']
    search_fields = ['student__email', 'course__title']
    ordering = ['-last_updated']
    readonly_fields = ['last_updated']