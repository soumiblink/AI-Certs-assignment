from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.utils import success_response
from vendor.models import Vendor
from product.models import Product
from course.models import Course
from certification.models import Certification


class DashboardStatsView(APIView):

    @swagger_auto_schema(
        operation_summary="Dashboard statistics",
        operation_description="Returns aggregate counts for all master entities.",
        responses={
            200: openapi.Response(
                description="Stats",
                examples={
                    "application/json": {
                        "success": True,
                        "data": {
                            "vendors": 10,
                            "products": 25,
                            "courses": 60,
                            "certifications": 30
                        }
                    }
                }
            )
        }
    )
    def get(self, request):
        data = {
            "vendors": Vendor.objects.count(),
            "products": Product.objects.count(),
            "courses": Course.objects.count(),
            "certifications": Certification.objects.count(),
        }
        return success_response(data)
