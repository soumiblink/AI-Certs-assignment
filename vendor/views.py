from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.utils import get_object_or_404_custom, success_response, error_response
from .models import Vendor
from .serializers import VendorSerializer


class VendorListCreateView(APIView):

    @swagger_auto_schema(
        operation_summary="List all vendors",
        responses={200: VendorSerializer(many=True)},
    )
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return success_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a vendor",
        request_body=VendorSerializer,
        responses={201: VendorSerializer},
    )
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status_code=201)
        return error_response(serializer.errors)


class VendorDetailView(APIView):

    @swagger_auto_schema(operation_summary="Retrieve a vendor", responses={200: VendorSerializer})
    def get(self, request, pk):
        vendor, err = get_object_or_404_custom(Vendor, pk=pk)
        if err:
            return err
        return success_response(VendorSerializer(vendor).data)

    @swagger_auto_schema(operation_summary="Update a vendor", request_body=VendorSerializer, responses={200: VendorSerializer})
    def put(self, request, pk):
        vendor, err = get_object_or_404_custom(Vendor, pk=pk)
        if err:
            return err
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(operation_summary="Partial update a vendor", request_body=VendorSerializer, responses={200: VendorSerializer})
    def patch(self, request, pk):
        vendor, err = get_object_or_404_custom(Vendor, pk=pk)
        if err:
            return err
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(operation_summary="Delete a vendor", responses={204: "No Content"})
    def delete(self, request, pk):
        vendor, err = get_object_or_404_custom(Vendor, pk=pk)
        if err:
            return err
        vendor.delete()
        return Response(status=204)
