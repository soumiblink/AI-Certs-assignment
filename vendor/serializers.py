from rest_framework import serializers
from .models import Vendor


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'code', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Name is required.")
        return value

    def validate_code(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Code is required.")
        qs = Vendor.objects.filter(code=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A vendor with this code already exists.")
        return value

    def get_validators(self):
        # Remove auto-generated unique validator for 'code' — handled manually above
        validators = super().get_validators()
        return [v for v in validators if not (
            hasattr(v, 'field_name') and v.field_name == 'code'
        )]
