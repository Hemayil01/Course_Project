from rest_framework import serializers
from datetime import datetime
import user
from .models import Course, Lesson, Enrollment, Progress



class CourseListModelSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.username', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'instructor_name', 'price', 'duration_days']
        read_only_fields = ['id', 'instructor_name']


class CourseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['id']

    def validate_duration_days(self, value):
        if value <= 0:
            raise serializers.ValidationError('Course duration must be greater than 0')
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('Course price cannot be negative')
        return value


class LessonModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['id']


class EnrollmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ['id', 'enrolled_at', 'end_date', 'status', 'student']

    def validate_course(self, value):
        user = self.context['request'].user
        if Enrollment.objects.filter(student=user, course=value, status=Enrollment.Status.ACTIVE).exists():
            raise serializers.ValidationError('You are already enrolled in this course')
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        return Enrollment.objects.create(student=user, **validated_data)


class ProgressModelSerializer(serializers.ModelSerializer):
    completion_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Progress
        fields = ['id', 'student', 'course', 'completed_lessons', 'completion_percentage', 'last_updated']
        read_only_fields = ['id', 'student', 'completion_percentage', 'last_updated']

    def get_completion_percentage(self, obj):
        return obj.completion_percentage()
    
    def create(self, validated_data):
        user = self.context['request'].user
        return Progress.objects.create(student=user, **validated_data)