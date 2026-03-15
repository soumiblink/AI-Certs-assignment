from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

uccess_response
from core.swagger_schemas import FULL_STRUCTURE_RESPONSE, ERROR_404
from vendor.models import Vendor
from vendor_product_mapping.models import VendorProductMapping
from product_course_mapping.models import ProductCourseMapping
from course_certification_mapping.models import CourseCertificationMapping


class VendorFullStructureView(APIView):

    @swagger_auto_schema(
        operation_summary="Get full vendor structure",
        operation_description=(
            "Returns the complete nested hierarchy for a vendor:\n\n"
            "Vendor → Products → Courses → Certifications\n\n"
            "Traverses VendorProductMapping → ProductCourseMapping → CourseCertificationMapping."
        ),
        responses={
            200: FULL_STRUCTURE_RESPONSE,
            404: ERROR_404,
        },
    )
    def get(self, request, vendor_id):
        vendor, err = get_object_or_404_custom(Vendor, pk=vendor_id)
        if err:
            return err

        vendor_product_mappings = (
            VendorProductMapping.objects
            .filter(vendor=vendor)
            .select_related('product')
        )

        products_data = []
        for vp_mapping in vendor_product_mappings:
            product = vp_mapping.product

            product_course_mappings = (
                ProductCourseMapping.objects
                .filter(product=product)
                .select_related('course')
            )

            courses_data = []
            for pc_mapping in product_course_mappings:
                course = pc_mapping.course

                course_cert_mappings = (
                    CourseCertificationMapping.objects
                    .filter(course=course)
                    .select_related('certification')
                )

                certifications = [cc.certification.name for cc in course_cert_mappings]
                courses_data.append({
                    "course": course.name,
                    "certifications": certifications,
                })

            products_data.append({
                "product": product.name,
                "courses": courses_data,
            })

        result = {
            "vendor": vendor.name,
            "products": products_data,
        }
        return success_response(result)
