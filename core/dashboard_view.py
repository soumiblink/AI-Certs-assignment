from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from core.utils import success_response
from core.swagger_schemas import DASHBOARD_RESPONSE
from vendor.models import Vendor
from product.models import Product
from course.models import Course
from certification.models import Certification


class DashboardStatsView(APIView):

    @swagger_auto_schema(
        operation_summary="Dashboard statistics",
        operation_description="Returns aggregate counts for all master entities: vendors, products, courses, certifications.",
        responses={
            200: DASHBOARD_RESPONSE,
        },
    )
    def get(self, request):
        data = {
            "vendors": Vendor.objects.count(),
            "products": Product.objects.count(),
            "courses": Course.objects.count(),
            "certifications": Certification.objects.count(),
        }
        return success_response(data)
