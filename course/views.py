from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.utils import get_object_or_404_custom, success_response, error_response
from .models import Course
from .serializers import CourseSerializer

product_id_param = openapi.Parameter('product_id', openapi.IN_QUERY, description="Filter by product ID", type=openapi.TYPE_INTEGER)


class CourseListCreateView(APIView):

    @swagger_auto_schema(
        operation_summary="List all courses",
        manual_parameters=[product_id_param],
        responses={200: CourseSerializer(many=True)},
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
        request_body=CourseSerializer,
        responses={201: CourseSerializer},
    )
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status_code=201)
        return error_response(serializer.errors)


class CourseDetailView(APIView):

    @swagger_auto_schema(operation_summary="Retrieve a course", responses={200: CourseSerializer})
    def get(self, request, pk):
        course, err = get_object_or_404_custom(Course, pk=pk)
        if err:
            return err
        return success_response(CourseSerializer(course).data)

    @swagger_auto_schema(operation_summary="Update a course", request_body=CourseSerializer, responses={200: CourseSerializer})
    def put(self, request, pk):
        course, err = get_object_or_404_custom(Course, pk=pk)
        if err:
            return err
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(operation_summary="Partial update a course", request_body=CourseSerializer, responses={200: CourseSerializer})
    def patch(self, request, pk):
        course, err = get_object_or_404_custom(Course, pk=pk)
        if err:
            return err
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(operation_summary="Delete a course", responses={204: "No Content"})
    def delete(self, request, pk):
        course, err = get_object_or_404_custom(Course, pk=pk)
        if err:
            return err
        course.delete()
        return success_response({"message": "Course deleted successfully."}, status_code=204)
