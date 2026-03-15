from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.utils import get_object_or_404_custom, success_response, error_response
from core.swagger_schemas import (
    PCM_LIST_RESPONSE, PCM_DETAIL_RESPONSE,
    ERROR_400, ERROR_404, NO_CONTENT_204,
)
from .models import ProductCourseMapping
from .serializers import ProductCourseMappingSerializer

product_id_param = openapi.Parameter(
    'product_id', openapi.IN_QUERY,
    description="Filter by product ID",
    type=openapi.TYPE_INTEGER,
    required=False,
)
course_id_param = openapi.Parameter(
    'course_id', openapi.IN_QUERY,
    description="Filter by course ID",
    type=openapi.TYPE_INTEGER,
    required=False,
)


class ProductCourseMappingListCreateView(APIView):

    @swagger_auto_schema(
        operation_summary="List product-course mappings",
        operation_description="Returns all product-course mappings. Supports filtering by `product_id` and/or `course_id`.",
        manual_parameters=[product_id_param, course_id_param],
        responses={
            200: PCM_LIST_RESPONSE,
        },
    )
    def get(self, request):
        qs = ProductCourseMapping.objects.select_related('product', 'course').all()
        product_id = request.query_params.get('product_id')
        course_id = request.query_params.get('course_id')
        if product_id:
            qs = qs.filter(product_id=product_id)
        if course_id:
            qs = qs.filter(course_id=course_id)
        serializer = ProductCourseMappingSerializer(qs, many=True)
        return success_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a product-course mapping",
        operation_description=(
            "Creates a new product-course mapping. "
            "Duplicate product+course pairs are rejected. "
            "Only one `primary_mapping=true` is allowed per product."
        ),
        request_body=ProductCourseMappingSerializer,
        responses={
            201: PCM_DETAIL_RESPONSE,
            400: ERROR_400,
        },
    )
    def post(self, request):
        serializer = ProductCourseMappingSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return success_response(ProductCourseMappingSerializer(instance).data, status_code=201)
        return error_response(serializer.errors)


class ProductCourseMappingDetailView(APIView):

    @swagger_auto_schema(
        operation_summary="Retrieve a product-course mapping",
        operation_description="Returns a single product-course mapping by ID.",
        responses={
            200: PCM_DETAIL_RESPONSE,
            404: ERROR_404,
        },
    )
    def get(self, request, pk):
        mapping, err = get_object_or_404_custom(ProductCourseMapping, pk=pk)
        if err:
            return err
        return success_response(ProductCourseMappingSerializer(mapping).data)

    @swagger_auto_schema(
        operation_summary="Update a product-course mapping",
        operation_description="Full update of a product-course mapping.",
        request_body=ProductCourseMappingSerializer,
        responses={
            200: PCM_DETAIL_RESPONSE,
            400: ERROR_400,
            404: ERROR_404,
        },
    )
    def put(self, request, pk):
        mapping, err = get_object_or_404_custom(ProductCourseMapping, pk=pk)
        if err:
            return err
        serializer = ProductCourseMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(
        operation_summary="Partial update a product-course mapping",
        operation_description="Partial update — only send fields you want to change.",
        request_body=ProductCourseMappingSerializer,
        responses={
            200: PCM_DETAIL_RESPONSE,
            400: ERROR_400,
            404: ERROR_404,
        },
    )
    def patch(self, request, pk):
        mapping, err = get_object_or_404_custom(ProductCourseMapping, pk=pk)
        if err:
            return err
        serializer = ProductCourseMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(
        operation_summary="Delete a product-course mapping",
        operation_description="Deletes a product-course mapping. Returns 204 with no body.",
        responses={
            204: NO_CONTENT_204,
            404: ERROR_404,
        },
    )
    def delete(self, request, pk):
        mapping, err = get_object_or_404_custom(ProductCourseMapping, pk=pk)
        if err:
            return err
        mapping.delete()
        return Response(status=204)
