from rest_framework import serializers
from .models import CourseCertificationMapping


class CourseCertificationMappingSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    certification_name = serializers.CharField(source='certification.name', read_only=True)

    class Meta:
        model = CourseCertificationMapping
        fields = [
            'id', 'course', 'course_name', 'certification', 'certification_name',
            'primary_mapping', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_validators(self):
        return []

    def validate(self, attrs):
        course = attrs.get('course', getattr(self.instance, 'course', None))
        certification = attrs.get('certification', getattr(self.instance, 'certification', None))

        # Prevent duplicate course+certification mapping
        qs = CourseCertificationMapping.objects.filter(course=course, certification=certification)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This course-certification mapping already exists.")

        # Enforce only one primary mapping per course
        if attrs.get('primary_mapping', getattr(self.instance, 'primary_mapping', False)):
            primary_qs = CourseCertificationMapping.objects.filter(course=course, primary_mapping=True)
            if self.instance:
                primary_qs = primary_qs.exclude(pk=self.instance.pk)
            if primary_qs.exists():
                raise serializers.ValidationError(
                    "This course already has a primary certification mapping. Only one primary mapping is allowed per course."
                )

        return attrs
