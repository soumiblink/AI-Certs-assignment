from django.contrib import admin
from .models import ProductCourseMapping


@admin.register(ProductCourseMapping)
class ProductCourseMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'course', 'primary_mapping', 'is_active', 'created_at')
    search_fields = ('product__name', 'course__name')
    list_filter = ('primary_mapping', 'is_active')
