from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.utils import get_object_or_404_custom, success_response, error_response
from .models import CourseCertificationMapping
from .serializers import CourseCertificationMappingSerializer

course_id_param = openapi.Parameter('course_id', openapi.IN_QUERY, description="Filter by course ID", type=openapi.TYPE_INTEGER)
cert_id_param = openapi.Parameter('certification_id', openapi.IN_QUERY, description="Filter by certification ID", type=openapi.TYPE_INTEGER)


class CourseCertificationMappingListCreateView(APIView):

    @swagger_auto_schema(
        operation_summary="List course-certification mappings",
        manual_parameters=[course_id_param, cert_id_param],
        responses={200: CourseCertificationMappingSerializer(many=True)},
    )
    def get(self, request):
        qs = CourseCertificationMapping.objects.select_related('course', 'certification').all()
        course_id = request.query_params.get('course_id')
        cert_id = request.query_params.get('certification_id')
        if course_id:
            qs = qs.filter(course_id=course_id)
        if cert_id:
            qs = qs.filter(certification_id=cert_id)
        serializer = CourseCertificationMappingSerializer(qs, many=True)
        return success_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a course-certification mapping",
        request_body=CourseCertificationMappingSerializer,
        responses={201: CourseCertificationMappingSerializer},
    )
    def post(self, request):
        serializer = CourseCertificationMappingSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return success_response(CourseCertificationMappingSerializer(instance).data, status_code=201)
        return error_response(serializer.errors)


class CourseCertificationMappingDetailView(APIView):

    @swagger_auto_schema(operation_summary="Retrieve a course-certification mapping", responses={200: CourseCertificationMappingSerializer})
    def get(self, request, pk):
        mapping, err = get_object_or_404_custom(CourseCertificationMapping, pk=pk)
        if err:
            return err
        return success_response(CourseCertificationMappingSerializer(mapping).data)

    @swagger_auto_schema(operation_summary="Update a course-certification mapping", request_body=CourseCertificationMappingSerializer, responses={200: CourseCertificationMappingSerializer})
    def put(self, request, pk):
        mapping, err = get_object_or_404_custom(CourseCertificationMapping, pk=pk)
        if err:
            return err
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(operation_summary="Partial update a course-certification mapping", request_body=CourseCertificationMappingSerializer, responses={200: CourseCertificationMappingSerializer})
    def patch(self, request, pk):
        mapping, err = get_object_or_404_custom(CourseCertificationMapping, pk=pk)
        if err:
            return err
        serializer = CourseCertificationMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(operation_summary="Delete a course-certification mapping", responses={204: "No Content"})
    def delete(self, request, pk):
        mapping, err = get_object_or_404_custom(CourseCertificationMapping, pk=pk)
        if err:
            return err
        mapping.delete()
        return Response(status=204)
