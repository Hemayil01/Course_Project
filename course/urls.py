from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views



router = DefaultRouter()
router.register('courses', views.CourseViewSet, basename='courses')
router.register('lessons', views.LessonViewSet, basename='lessons')


urlpatterns = [
    path('health_check/', views.HealthCheckAPIView.as_view(), name='health-check'),
    path('enroll/', views.EnrollmentAPIView.as_view(), name='enroll-course'),
    path('enrollments/', views.EnrollmentAPIView.as_view(), name='enrollment-list'),
    path('enroll/<int:course_id>/', views.EnrollmentAPIView.as_view(), name='enroll-course-detail'),
    path('progress/<int:course_id>/', views.ProgressAPIView.as_view(), name='course-progress'),
]


urlpatterns += router.urls

"""
courses/ - list courses
courses/ - create course
courses/<id>/ - retrieve | update | partial_update | destroy
lessons/ - list lessons
lessons/<id>/ - retrieve | update | partial_update | destroy
health_check/ - API health check
enroll/ - enroll in a course {'course': 1}
enrollments/ - list all enrollments (student, instructor, admin)
enroll/<course_id>/ - enroll in specific course / return enrollment info
progress/<course_id>/ - get or update progress for a course

"""