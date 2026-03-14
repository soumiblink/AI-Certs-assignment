from django.core.management.base import BaseCommand
from vendor.models import Vendor
from product.models import Product
from course.models import Course
from certification.models import Certification
from vendor_product_mapping.models import VendorProductMapping
from product_course_mapping.models import ProductCourseMapping
from course_certification_mapping.models import CourseCertificationMapping


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Vendors
        v1, _ = Vendor.objects.get_or_create(code='MSFT', defaults={'name': 'Microsoft', 'description': 'Microsoft Corporation'})
        v2, _ = Vendor.objects.get_or_create(code='AMZN', defaults={'name': 'Amazon', 'description': 'Amazon Web Services'})
        v3, _ = Vendor.objects.get_or_create(code='GOOG', defaults={'name': 'Google', 'description': 'Google Cloud'})

        # Products
        p1, _ = Product.objects.get_or_create(code='AZURE', defaults={'name': 'Azure', 'description': 'Microsoft Azure Cloud'})
        p2, _ = Product.objects.get_or_create(code='AWS', defaults={'name': 'AWS', 'description': 'Amazon Web Services'})
        p3, _ = Product.objects.get_or_create(code='GCP', defaults={'name': 'GCP', 'description': 'Google Cloud Platform'})
        p4, _ = Product.objects.get_or_create(code='M365', defaults={'name': 'Microsoft 365', 'description': 'Microsoft 365 Suite'})

        # Courses
        c1, _ = Course.objects.get_or_create(code='AZ-900-C', defaults={'name': 'Azure Fundamentals', 'description': 'Intro to Azure'})
        c2, _ = Course.objects.get_or_create(code='AZ-104-C', defaults={'name': 'Azure Administrator', 'description': 'Azure Admin course'})
        c3, _ = Course.objects.get_or_create(code='AWS-CCP-C', defaults={'name': 'AWS Cloud Practitioner', 'description': 'AWS intro course'})
        c4, _ = Course.objects.get_or_create(code='GCP-ACE-C', defaults={'name': 'GCP Associate Engineer', 'description': 'GCP core course'})

        # Certifications
        cert1, _ = Certification.objects.get_or_create(code='AZ-900', defaults={'name': 'AZ-900', 'description': 'Azure Fundamentals Cert'})
        cert2, _ = Certification.objects.get_or_create(code='AZ-104', defaults={'name': 'AZ-104', 'description': 'Azure Administrator Cert'})
        cert3, _ = Certification.objects.get_or_create(code='AWS-CCP', defaults={'name': 'AWS-CCP', 'description': 'AWS Cloud Practitioner Cert'})
        cert4, _ = Certification.objects.get_or_create(code='GCP-ACE', defaults={'name': 'GCP-ACE', 'description': 'GCP Associate Cloud Engineer'})

        # Vendor-Product Mappings
        VendorProductMapping.objects.get_or_create(vendor=v1, product=p1, defaults={'primary_mapping': True})
        VendorProductMapping.objects.get_or_create(vendor=v1, product=p4, defaults={'primary_mapping': False})
        VendorProductMapping.objects.get_or_create(vendor=v2, product=p2, defaults={'primary_mapping': True})
        VendorProductMapping.objects.get_or_create(vendor=v3, product=p3, defaults={'primary_mapping': True})

        # Product-Course Mappings
        ProductCourseMapping.objects.get_or_create(product=p1, course=c1, defaults={'primary_mapping': True})
        ProductCourseMapping.objects.get_or_create(product=p1, course=c2, defaults={'primary_mapping': False})
        ProductCourseMapping.objects.get_or_create(product=p2, course=c3, defaults={'primary_mapping': True})
        ProductCourseMapping.objects.get_or_create(product=p3, course=c4, defaults={'primary_mapping': True})

        # Course-Certification Mappings
        CourseCertificationMapping.objects.get_or_create(course=c1, certification=cert1, defaults={'primary_mapping': True})
        CourseCertificationMapping.objects.get_or_create(course=c2, certification=cert2, defaults={'primary_mapping': True})
        CourseCertificationMapping.objects.get_or_create(course=c3, certification=cert3, defaults={'primary_mapping': True})
        CourseCertificationMapping.objects.get_or_create(course=c4, certification=cert4, defaults={'primary_mapping': True})

        self.stdout.write(self.style.SUCCESS('Seed data created successfully.'))
