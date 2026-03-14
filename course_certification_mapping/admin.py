from django.contrib import admin
from .models import CourseCertificationMapping


@admin.register(CourseCertificationMapping)
class CourseCertificationMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'certification', 'primary_mapping', 'is_active', 'created_at')
    search_fields = ('course__name', 'certification__name')
    list_filter = ('primary_mapping', 'is_active')
