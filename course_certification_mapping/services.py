from .models import CourseCertificationMapping
from .serializers import CourseCertificationMappingSerializer


def create_course_certification_mapping(data):
    """Create a new CourseCertificationMapping after validation."""
    serializer = CourseCertificationMappingSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def validate_primary_course_certification(course, exclude_instance=None):
    """
    Check if a course already has a primary certification mapping.
    Returns True if a primary mapping exists (conflict), False otherwise.
    """
    qs = CourseCertificationMapping.objects.filter(course=course, primary_mapping=True)
    if exclude_instance:
        qs = qs.exclude(pk=exclude_instance.pk)
    return qs.exists()


def update_course_certification_mapping(instance, data, partial=False):
    """Update an existing CourseCertificationMapping."""
    serializer = CourseCertificationMappingSerializer(instance, data=data, partial=partial)
    serializer.is_valid(raise_exception=True)
    return serializer.save()
