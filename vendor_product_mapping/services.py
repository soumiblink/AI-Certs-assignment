from .models import VendorProductMapping
from .serializers import VendorProductMappingSerializer


def create_vendor_product_mapping(data):
    """Create a new VendorProductMapping after validation."""
    serializer = VendorProductMappingSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def validate_primary_vendor_product(vendor, exclude_instance=None):
    """
    Check if a vendor already has a primary product mapping.
    Returns True if a primary mapping exists (conflict), False otherwise.
    """
    qs = VendorProductMapping.objects.filter(vendor=vendor, primary_mapping=True)
    if exclude_instance:
        qs = qs.exclude(pk=exclude_instance.pk)
    return qs.exists()


def update_vendor_product_mapping(instance, data, partial=False):
    """Update an existing VendorProductMapping."""
    serializer = VendorProductMappingSerializer(instance, data=data, partial=partial)
    serializer.is_valid(raise_exception=True)
    return serializer.save()
