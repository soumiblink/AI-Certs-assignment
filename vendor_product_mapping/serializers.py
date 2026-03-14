from rest_framework import serializers
from .models import VendorProductMapping


class VendorProductMappingSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = VendorProductMapping
        fields = [
            'id', 'vendor', 'vendor_name', 'product', 'product_name',
            'primary_mapping', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        vendor = attrs.get('vendor', getattr(self.instance, 'vendor', None))
        product = attrs.get('product', getattr(self.instance, 'product', None))

        # Prevent duplicate vendor+product mapping
        qs = VendorProductMapping.objects.filter(vendor=vendor, product=product)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This vendor-product mapping already exists.")

        # Enforce only one primary mapping per vendor
        if attrs.get('primary_mapping', False):
            primary_qs = VendorProductMapping.objects.filter(vendor=vendor, primary_mapping=True)
            if self.instance:
                primary_qs = primary_qs.exclude(pk=self.instance.pk)
            if primary_qs.exists():
                raise serializers.ValidationError(
                    "This vendor already has a primary product mapping. Only one primary mapping is allowed per vendor."
                )

        return attrs
