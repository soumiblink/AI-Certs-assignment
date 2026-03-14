from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Name is required.")
        return value

    def validate_code(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Code is required.")
        qs = Course.objects.filter(code=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A course with this code already exists.")
        return value

    def get_validators(self):
        validators = super().get_validators()
        return [v for v in validators if not (
            hasattr(v, 'field_name') and v.field_name == 'code'
        )]
