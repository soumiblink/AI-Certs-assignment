from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.utils import get_object_or_404_custom, success_response, error_response
from .models import VendorProductMapping
from .serializers import VendorProductMappingSerializer

vendor_id_param = openapi.Parameter('vendor_id', openapi.IN_QUERY, description="Filter by vendor ID", type=openapi.TYPE_INTEGER)
product_id_param = openapi.Parameter('product_id', openapi.IN_QUERY, description="Filter by product ID", type=openapi.TYPE_INTEGER)


class VendorProductMappingListCreateView(APIView):

    @swagger_auto_schema(
        operation_summary="List vendor-product mappings",
        manual_parameters=[vendor_id_param, product_id_param],
        responses={200: VendorProductMappingSerializer(many=True)},
    )
    def get(self, request):
        qs = VendorProductMapping.objects.select_related('vendor', 'product').all()
        vendor_id = request.query_params.get('vendor_id')
        product_id = request.query_params.get('product_id')
        if vendor_id:
            qs = qs.filter(vendor_id=vendor_id)
        if product_id:
            qs = qs.filter(product_id=product_id)
        serializer = VendorProductMappingSerializer(qs, many=True)
        return success_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a vendor-product mapping",
        request_body=VendorProductMappingSerializer,
        responses={201: VendorProductMappingSerializer},
    )
    def post(self, request):
        serializer = VendorProductMappingSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return success_response(VendorProductMappingSerializer(instance).data, status_code=201)
        return error_response(serializer.errors)


class VendorProductMappingDetailView(APIView):

    @swagger_auto_schema(operation_summary="Retrieve a vendor-product mapping", responses={200: VendorProductMappingSerializer})
    def get(self, request, pk):
        mapping, err = get_object_or_404_custom(VendorProductMapping, pk=pk)
        if err:
            return err
        return success_response(VendorProductMappingSerializer(mapping).data)

    @swagger_auto_schema(operation_summary="Update a vendor-product mapping", request_body=VendorProductMappingSerializer, responses={200: VendorProductMappingSerializer})
    def put(self, request, pk):
        mapping, err = get_object_or_404_custom(VendorProductMapping, pk=pk)
        if err:
            return err
        serializer = VendorProductMappingSerializer(mapping, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(operation_summary="Partial update a vendor-product mapping", request_body=VendorProductMappingSerializer, responses={200: VendorProductMappingSerializer})
    def patch(self, request, pk):
        mapping, err = get_object_or_404_custom(VendorProductMapping, pk=pk)
        if err:
            return err
        serializer = VendorProductMappingSerializer(mapping, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(operation_summary="Delete a vendor-product mapping", responses={204: "No Content"})
    def delete(self, request, pk):
        mapping, err = get_object_or_404_custom(VendorProductMapping, pk=pk)
        if err:
            return err
        mapping.delete()
        return Response(status=204)
