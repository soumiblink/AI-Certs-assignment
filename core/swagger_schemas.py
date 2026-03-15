"""
Reusable drf-yasg schema builders that match the actual API response envelope:

  Success:  {"success": true,  "data": <payload>}
  Error:    {"success": false, "message": <detail>}
  404:      {"success": false, "message": "<Model> not found"}
  204:      (empty body)
"""
from drf_yasg import openapi



SUCCESS_FIELD = openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True)
SUCCESS_FALSE = openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False)



ERROR_400 = openapi.Response(
    description="Validation error",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
            "message": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description="Field-level validation errors",
                example={"field_name": ["This field is required."]},
            ),
        },
        required=["success", "message"],
    ),
)

ERROR_404 = openapi.Response(
    description="Not found",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
            "message": openapi.Schema(type=openapi.TYPE_STRING, example="Object not found"),
        },
        required=["success", "message"],
    ),
)

NO_CONTENT_204 = openapi.Response(description="Deleted successfully — no content returned")




def success_list_schema(item_schema: openapi.Schema, description: str = "Success") -> openapi.Response:
    """Wraps an array of items: {"success": true, "data": [...]}"""
    return openapi.Response(
        description=description,
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "success": SUCCESS_FIELD,
                "data": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=item_schema,
                ),
            },
            required=["success", "data"],
        ),
    )


def success_detail_schema(item_schema: openapi.Schema, description: str = "Success") -> openapi.Response:
    """Wraps a single object: {"success": true, "data": {...}}"""
    return openapi.Response(
        description=description,
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "success": SUCCESS_FIELD,
                "data": item_schema,
            },
            required=["success", "data"],
        ),
    )




def _base_master_fields(model_name: str) -> dict:
    return {
        "id":          openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
        "name":        openapi.Schema(type=openapi.TYPE_STRING,  example=model_name),
        "code":        openapi.Schema(type=openapi.TYPE_STRING,  example=f"{model_name.upper()[:3]}-001"),
        "description": openapi.Schema(type=openapi.TYPE_STRING,  example=f"{model_name} description"),
        "is_active":   openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
        "created_at":  openapi.Schema(type=openapi.TYPE_STRING,  format=openapi.FORMAT_DATETIME),
        "updated_at":  openapi.Schema(type=openapi.TYPE_STRING,  format=openapi.FORMAT_DATETIME),
    }


VENDOR_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties=_base_master_fields("Vendor"),
)

PRODUCT_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties=_base_master_fields("Product"),
)

COURSE_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties=_base_master_fields("Course"),
)

CERTIFICATION_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties=_base_master_fields("Certification"),
)

VENDOR_PRODUCT_MAPPING_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id":             openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
        "vendor":         openapi.Schema(type=openapi.TYPE_INTEGER, example=1, description="Vendor ID"),
        "vendor_name":    openapi.Schema(type=openapi.TYPE_STRING,  example="Microsoft"),
        "product":        openapi.Schema(type=openapi.TYPE_INTEGER, example=1, description="Product ID"),
        "product_name":   openapi.Schema(type=openapi.TYPE_STRING,  example="Azure"),
        "primary_mapping":openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
        "is_active":      openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
        "created_at":     openapi.Schema(type=openapi.TYPE_STRING,  format=openapi.FORMAT_DATETIME),
        "updated_at":     openapi.Schema(type=openapi.TYPE_STRING,  format=openapi.FORMAT_DATETIME),
    },
)

PRODUCT_COURSE_MAPPING_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id":             openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
        "product":        openapi.Schema(type=openapi.TYPE_INTEGER, example=1, description="Product ID"),
        "product_name":   openapi.Schema(type=openapi.TYPE_STRING,  example="Azure"),
        "course":         openapi.Schema(type=openapi.TYPE_INTEGER, example=1, description="Course ID"),
        "course_name":    openapi.Schema(type=openapi.TYPE_STRING,  example="Azure Fundamentals"),
        "primary_mapping":openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
        "is_active":      openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
        "created_at":     openapi.Schema(type=openapi.TYPE_STRING,  format=openapi.FORMAT_DATETIME),
        "updated_at":     openapi.Schema(type=openapi.TYPE_STRING,  format=openapi.FORMAT_DATETIME),
    },
)

COURSE_CERTIFICATION_MAPPING_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id":                  openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
        "course":              openapi.Schema(type=openapi.TYPE_INTEGER, example=1, description="Course ID"),
        "course_name":         openapi.Schema(type=openapi.TYPE_STRING,  example="Azure Fundamentals"),
        "certification":       openapi.Schema(type=openapi.TYPE_INTEGER, example=1, description="Certification ID"),
        "certification_name":  openapi.Schema(type=openapi.TYPE_STRING,  example="AZ-900"),
        "primary_mapping":     openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
        "is_active":           openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
        "created_at":          openapi.Schema(type=openapi.TYPE_STRING,  format=openapi.FORMAT_DATETIME),
        "updated_at":          openapi.Schema(type=openapi.TYPE_STRING,  format=openapi.FORMAT_DATETIME),
    },
)



# Vendor
VENDOR_LIST_RESPONSE    = success_list_schema(VENDOR_SCHEMA,   "List of vendors")
VENDOR_DETAIL_RESPONSE  = success_detail_schema(VENDOR_SCHEMA, "Vendor detail")

# Product
PRODUCT_LIST_RESPONSE   = success_list_schema(PRODUCT_SCHEMA,   "List of products")
PRODUCT_DETAIL_RESPONSE = success_detail_schema(PRODUCT_SCHEMA, "Product detail")

# Course
COURSE_LIST_RESPONSE    = success_list_schema(COURSE_SCHEMA,   "List of courses")
COURSE_DETAIL_RESPONSE  = success_detail_schema(COURSE_SCHEMA, "Course detail")

# Certification
CERTIFICATION_LIST_RESPONSE   = success_list_schema(CERTIFICATION_SCHEMA,   "List of certifications")
CERTIFICATION_DETAIL_RESPONSE = success_detail_schema(CERTIFICATION_SCHEMA, "Certification detail")

# VendorProductMapping
VPM_LIST_RESPONSE   = success_list_schema(VENDOR_PRODUCT_MAPPING_SCHEMA,   "List of vendor-product mappings")
VPM_DETAIL_RESPONSE = success_detail_schema(VENDOR_PRODUCT_MAPPING_SCHEMA, "Vendor-product mapping detail")

# ProductCourseMapping
PCM_LIST_RESPONSE   = success_list_schema(PRODUCT_COURSE_MAPPING_SCHEMA,   "List of product-course mappings")
PCM_DETAIL_RESPONSE = success_detail_schema(PRODUCT_COURSE_MAPPING_SCHEMA, "Product-course mapping detail")

# CourseCertificationMapping
CCM_LIST_RESPONSE   = success_list_schema(COURSE_CERTIFICATION_MAPPING_SCHEMA,   "List of course-certification mappings")
CCM_DETAIL_RESPONSE = success_detail_schema(COURSE_CERTIFICATION_MAPPING_SCHEMA, "Course-certification mapping detail")

# Full structure
_CERT_ITEM = openapi.Schema(type=openapi.TYPE_STRING, example="AZ-900")
_COURSE_ITEM = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "course":         openapi.Schema(type=openapi.TYPE_STRING, example="Azure Fundamentals"),
        "certifications": openapi.Schema(type=openapi.TYPE_ARRAY, items=_CERT_ITEM),
    },
)
_PRODUCT_ITEM = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "product": openapi.Schema(type=openapi.TYPE_STRING, example="Azure"),
        "courses": openapi.Schema(type=openapi.TYPE_ARRAY, items=_COURSE_ITEM),
    },
)
FULL_STRUCTURE_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "vendor":   openapi.Schema(type=openapi.TYPE_STRING, example="Microsoft"),
        "products": openapi.Schema(type=openapi.TYPE_ARRAY, items=_PRODUCT_ITEM),
    },
)
FULL_STRUCTURE_RESPONSE = success_detail_schema(FULL_STRUCTURE_SCHEMA, "Full vendor structure")


DASHBOARD_SCHEMA = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "vendors":        openapi.Schema(type=openapi.TYPE_INTEGER, example=10),
        "products":       openapi.Schema(type=openapi.TYPE_INTEGER, example=25),
        "courses":        openapi.Schema(type=openapi.TYPE_INTEGER, example=60),
        "certifications": openapi.Schema(type=openapi.TYPE_INTEGER, example=30),
    },
)
DASHBOARD_RESPONSE = success_detail_schema(DASHBOARD_SCHEMA, "Dashboard statistics")
