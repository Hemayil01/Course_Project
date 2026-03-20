from django.db import models
from datetime import timedelta
from django.utils import timezone
from user.models import User


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    duration_days = models.PositiveIntegerField(default=30)

    def __str__(self):
        return f'{self.title} ({self.instructor.username})'

    def student_count(self):
        return self.enrollments.count()


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField()
    order = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.course.title} - {self.title}'


class Enrollment(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    def __str__(self):
        return f'{self.student.email} - {self.course.title}'

    def is_active(self):
        return self.status == self.Status.ACTIVE and timezone.now() < self.end_date

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = timezone.now() + timedelta(days=self.course.duration_days)
        super().save(*args, **kwargs)


class Progress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='progress')
    completed_lessons = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.student.email} - {self.course.title}'

    def completion_percentage(self):
        total_lessons = self.course.lessons.count()
        if total_lessons == 0:
            return 0
        return (self.completed_lessons / total_lessons) * 100
    

class Progress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='progress')
    completed_lessons = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.student.email} - {self.course.title}'

    def completion_percentage(self):
        total_lessons = self.course.lessons.count()
        if total_lessons == 0:
            return 0
        return (self.completed_lessons / total_lessons) * 100
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'course'], name='unique_progress')]