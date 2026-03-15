from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.utils import get_object_or_404_custom, success_response, error_response
from core.swagger_schemas import (
    CERTIFICATION_LIST_RESPONSE, CERTIFICATION_DETAIL_RESPONSE,
    ERROR_400, ERROR_404, NO_CONTENT_204,
)
from .models import Certification
from .serializers import CertificationSerializer

course_id_param = openapi.Parameter(
    'course_id', openapi.IN_QUERY,
    description="Filter certifications by course ID (via CourseCertificationMapping)",
    type=openapi.TYPE_INTEGER,
    required=False,
)


class CertificationListCreateView(APIView):

    @swagger_auto_schema(
        operation_summary="List all certifications",
        operation_description="Returns all certifications. Filter by `course_id` to get certifications linked to a specific course.",
        manual_parameters=[course_id_param],
        responses={
            200: CERTIFICATION_LIST_RESPONSE,
        },
    )
    def get(self, request):
        certifications = Certification.objects.all()
        course_id = request.query_params.get('course_id')
        if course_id:
            certifications = certifications.filter(course_certification_mappings__course_id=course_id)
        serializer = CertificationSerializer(certifications, many=True)
        return success_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a certification",
        operation_description="Creates a new certification. Code must be unique.",
        request_body=CertificationSerializer,
        responses={
            201: CERTIFICATION_DETAIL_RESPONSE,
            400: ERROR_400,
        },
    )
    def post(self, request):
        serializer = CertificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status_code=201)
        return error_response(serializer.errors)


class CertificationDetailView(APIView):

    @swagger_auto_schema(
        operation_summary="Retrieve a certification",
        operation_description="Returns a single certification by ID.",
        responses={
            200: CERTIFICATION_DETAIL_RESPONSE,
            404: ERROR_404,
        },
    )
    def get(self, request, pk):
        cert, err = get_object_or_404_custom(Certification, pk=pk)
        if err:
            return err
        return success_response(CertificationSerializer(cert).data)

    @swagger_auto_schema(
        operation_summary="Update a certification",
        operation_description="Full update of a certification. All fields required.",
        request_body=CertificationSerializer,
        responses={
            200: CERTIFICATION_DETAIL_RESPONSE,
            400: ERROR_400,
            404: ERROR_404,
        },
    )
    def put(self, request, pk):
        cert, err = get_object_or_404_custom(Certification, pk=pk)
        if err:
            return err
        serializer = CertificationSerializer(cert, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(
        operation_summary="Partial update a certification",
        operation_description="Partial update — only send fields you want to change.",
        request_body=CertificationSerializer,
        responses={
            200: CERTIFICATION_DETAIL_RESPONSE,
            400: ERROR_400,
            404: ERROR_404,
        },
    )
    def patch(self, request, pk):
        cert, err = get_object_or_404_custom(Certification, pk=pk)
        if err:
            return err
        serializer = CertificationSerializer(cert, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(
        operation_summary="Delete a certification",
        operation_description="Deletes a certification. Returns 204 with no body.",
        responses={
            204: NO_CONTENT_204,
            404: ERROR_404,
        },
    )
    def delete(self, request, pk):
        cert, err = get_object_or_404_custom(Certification, pk=pk)
        if err:
            return err
        cert.delete()
        return Response(status=204)
