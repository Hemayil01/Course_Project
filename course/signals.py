from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Course, Lesson, Enrollment, Progress
from django.utils import timezone



@receiver(post_save, sender=Course)
def inform_about_course(sender, instance, created, **kwargs):
    if created:
        print('New course created:', instance.title)
    else:
        print('Course updated:', instance.title)


@receiver(pre_save, sender=Course)
def validate_course(sender, instance, **kwargs):
    if instance.price < 0:
        raise ValueError('Course price cannot be negative')
    if instance.duration_days <= 0:
        raise ValueError('Course duration must be greater than 0')


@receiver(post_save, sender=Lesson)
def inform_about_lesson(sender, instance, created, **kwargs):
    if created:
        print('New lesson created for course:', instance.course.title)
    else:
        print('Lesson updated for course:', instance.course.title)


@receiver(pre_save, sender=Lesson)
def validate_lesson(sender, instance, **kwargs):
    if instance.order <= 0:
        raise ValueError('Lesson order must be greater than 0')


@receiver(post_save, sender=Enrollment)
def inform_about_enrollment(sender, instance, created, **kwargs):
    if created:
        print(f'Student {instance.student.email} enrolled in course: {instance.course.title}')
    else:
        print(f'Enrollment updated for student {instance.student.email} in course: {instance.course.title}')


@receiver(pre_save, sender=Enrollment)
def validate_enrollment(sender, instance, **kwargs):
    if instance.end_date and instance.end_date < timezone.now():
        raise ValueError('End date cannot be in the past')

@receiver(post_save, sender=Progress)
def inform_about_progress(sender, instance, created, **kwargs):
    if created:
        print(f'New progress created for student {instance.student.email} in course {instance.course.title}')
    else:
        print(f'Progress updated for student {instance.student.email} in course {instance.course.title}')
