from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.utils import get_object_or_404_custom, success_response, error_response
from core.swagger_schemas import (
    COURSE_LIST_RESPONSE, COURSE_DETAIL_RESPONSE,
    ERROR_400, ERROR_404, NO_CONTENT_204,
)
from .models import Course
from .serializers import CourseSerializer

product_id_param = openapi.Parameter(
    'product_id', openapi.IN_QUERY,
    description="Filter courses by product ID (via ProductCourseMapping)",
    type=openapi.TYPE_INTEGER,
    required=False,
)


class CourseListCreateView(APIView):

    @swagger_auto_schema(
        operation_summary="List all courses",
        operation_description="Returns all courses. Filter by `product_id` to get courses linked to a specific product.",
        manual_parameters=[product_id_param],
        responses={
            200: COURSE_LIST_RESPONSE,
        },
    )
    def get(self, request):
        courses = Course.objects.all()
        product_id = request.query_params.get('product_id')
        if product_id:
            courses = courses.filter(product_course_mappings__product_id=product_id)
        serializer = CourseSerializer(courses, many=True)
        return success_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a course",
        operation_description="Creates a new course. Code must be unique.",
        request_body=CourseSerializer,
        responses={
            201: COURSE_DETAIL_RESPONSE,
            400: ERROR_400,
        },
    )
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status_code=201)
        return error_response(serializer.errors)


class CourseDetailView(APIView):

    @swagger_auto_schema(
        operation_summary="Retrieve a course",
        operation_description="Returns a single course by ID.",
        responses={
            200: COURSE_DETAIL_RESPONSE,
            404: ERROR_404,
        },
    )
    def get(self, request, pk):
        course, err = get_object_or_404_custom(Course, pk=pk)
        if err:
            return err
        return success_response(CourseSerializer(course).data)

    @swagger_auto_schema(
        operation_summary="Update a course",
        operation_description="Full update of a course. All fields required.",
        request_body=CourseSerializer,
        responses={
            200: COURSE_DETAIL_RESPONSE,
            400: ERROR_400,
            404: ERROR_404,
        },
    )
    def put(self, request, pk):
        course, err = get_object_or_404_custom(Course, pk=pk)
        if err:
            return err
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(
        operation_summary="Partial update a course",
        operation_description="Partial update — only send fields you want to change.",
        request_body=CourseSerializer,
        responses={
            200: COURSE_DETAIL_RESPONSE,
            400: ERROR_400,
            404: ERROR_404,
        },
    )
    def patch(self, request, pk):
        course, err = get_object_or_404_custom(Course, pk=pk)
        if err:
            return err
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(
        operation_summary="Delete a course",
        operation_description="Deletes a course. Returns 204 with no body.",
        responses={
            204: NO_CONTENT_204,
            404: ERROR_404,
        },
    )
    def delete(self, request, pk):
        course, err = get_object_or_404_custom(Course, pk=pk)
        if err:
            return err
        course.delete()
        return Response(status=204)
