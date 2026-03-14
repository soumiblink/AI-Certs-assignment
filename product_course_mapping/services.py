from .models import ProductCourseMapping
from .serializers import ProductCourseMappingSerializer


def create_product_course_mapping(data):
    """Create a new ProductCourseMapping after validation."""
    serializer = ProductCourseMappingSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def validate_primary_product_course(product, exclude_instance=None):
    """
    Check if a product already has a primary course mapping.
    Returns True if a primary mapping exists (conflict), False otherwise.
    """
    qs = ProductCourseMapping.objects.filter(product=product, primary_mapping=True)
    if exclude_instance:
        qs = qs.exclude(pk=exclude_instance.pk)
    return qs.exists()


def update_product_course_mapping(instance, data, partial=False):
    """Update an existing ProductCourseMapping."""
    serializer = ProductCourseMappingSerializer(instance, data=data, partial=partial)
    serializer.is_valid(raise_exception=True)
    return serializer.save()
