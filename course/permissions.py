from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated


class IsAdminOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'


class IsInstructorOrAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['instructor', 'admin']



class IsStudentOrAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['student', 'admin']


class IsOwnerOrAdmin(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and (
            request.user.role == 'admin' or
            getattr(obj, 'student', None) == request.user
        )


class CanManageCourses(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.role == 'admin':
            return True
        if request.user.role == 'instructor':
            return request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
        if request.user.role == 'student':
            return request.method in permissions.SAFE_METHODS
        return False



class CanManageLessons(IsAuthenticated):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.role == 'admin':
            return True
        if request.user.role == 'instructor':
            return True
        if request.user.role == 'student':
            return request.method in permissions.SAFE_METHODS
        return False

class CanManageEnrollments(IsAuthenticated):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['instructor', 'admin']
    
class CanManageProgress(IsAuthenticated):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['student', 'instructor', 'admin']

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'student':
            return obj.student == request.user
        return request.user.role in ['instructor', 'admin']