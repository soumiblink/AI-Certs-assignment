from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.utils import get_object_or_404_custom, success_response, error_response
from .models import Certification
from .serializers import CertificationSerializer

course_id_param = openapi.Parameter('course_id', openapi.IN_QUERY, description="Filter by course ID", type=openapi.TYPE_INTEGER)


class CertificationListCreateView(APIView):

    @swagger_auto_schema(
        operation_summary="List all certifications",
        manual_parameters=[course_id_param],
        responses={200: CertificationSerializer(many=True)},
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
        request_body=CertificationSerializer,
        responses={201: CertificationSerializer},
    )
    def post(self, request):
        serializer = CertificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status_code=201)
        return error_response(serializer.errors)


class CertificationDetailView(APIView):

    @swagger_auto_schema(operation_summary="Retrieve a certification", responses={200: CertificationSerializer})
    def get(self, request, pk):
        cert, err = get_object_or_404_custom(Certification, pk=pk)
        if err:
            return err
        return success_response(CertificationSerializer(cert).data)

    @swagger_auto_schema(operation_summary="Update a certification", request_body=CertificationSerializer, responses={200: CertificationSerializer})
    def put(self, request, pk):
        cert, err = get_object_or_404_custom(Certification, pk=pk)
        if err:
            return err
        serializer = CertificationSerializer(cert, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(operation_summary="Partial update a certification", request_body=CertificationSerializer, responses={200: CertificationSerializer})
    def patch(self, request, pk):
        cert, err = get_object_or_404_custom(Certification, pk=pk)
        if err:
            return err
        serializer = CertificationSerializer(cert, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(operation_summary="Delete a certification", responses={204: "No Content"})
    def delete(self, request, pk):
        cert, err = get_object_or_404_custom(Certification, pk=pk)
        if err:
            return err
        cert.delete()
        return Response(status=204)
