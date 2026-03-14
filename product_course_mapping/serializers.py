from rest_framework import serializers
from .models import ProductCourseMapping


class ProductCourseMappingSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = ProductCourseMapping
        fields = [
            'id', 'product', 'product_name', 'course', 'course_name',
            'primary_mapping', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        product = attrs.get('product', getattr(self.instance, 'product', None))
        course = attrs.get('course', getattr(self.instance, 'course', None))

        # Prevent duplicate product+course mapping
        qs = ProductCourseMapping.objects.filter(product=product, course=course)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This product-course mapping already exists.")

        # Enforce only one primary mapping per product
        if attrs.get('primary_mapping', False):
            primary_qs = ProductCourseMapping.objects.filter(product=product, primary_mapping=True)
            if self.instance:
                primary_qs = primary_qs.exclude(pk=self.instance.pk)
            if primary_qs.exists():
                raise serializers.ValidationError(
                    "This product already has a primary course mapping. Only one primary mapping is allowed per product."
                )

        return attrs
