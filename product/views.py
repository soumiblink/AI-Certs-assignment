from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.utils import get_object_or_404_custom, success_response, error_response
from core.swagger_schemas import (
    PRODUCT_LIST_RESPONSE, PRODUCT_DETAIL_RESPONSE,
    ERROR_400, ERROR_404, NO_CONTENT_204,
)
from .models import Product
from .serializers import ProductSerializer

vendor_id_param = openapi.Parameter(
    'vendor_id', openapi.IN_QUERY,
    description="Filter products by vendor ID (via VendorProductMapping)",
    type=openapi.TYPE_INTEGER,
    required=False,
)


class ProductListCreateView(APIView):

    @swagger_auto_schema(
        operation_summary="List all products",
        operation_description="Returns all products. Filter by `vendor_id` to get products linked to a specific vendor.",
        manual_parameters=[vendor_id_param],
        responses={
            200: PRODUCT_LIST_RESPONSE,
        },
    )
    def get(self, request):
        products = Product.objects.all()
        vendor_id = request.query_params.get('vendor_id')
        if vendor_id:
            products = products.filter(vendor_product_mappings__vendor_id=vendor_id)
        serializer = ProductSerializer(products, many=True)
        return success_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a product",
        operation_description="Creates a new product. Code must be unique.",
        request_body=ProductSerializer,
        responses={
            201: PRODUCT_DETAIL_RESPONSE,
            400: ERROR_400,
        },
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status_code=201)
        return error_response(serializer.errors)


class ProductDetailView(APIView):

    @swagger_auto_schema(
        operation_summary="Retrieve a product",
        operation_description="Returns a single product by ID.",
        responses={
            200: PRODUCT_DETAIL_RESPONSE,
            404: ERROR_404,
        },
    )
    def get(self, request, pk):
        product, err = get_object_or_404_custom(Product, pk=pk)
        if err:
            return err
        return success_response(ProductSerializer(product).data)

    @swagger_auto_schema(
        operation_summary="Update a product",
        operation_description="Full update of a product. All fields required.",
        request_body=ProductSerializer,
        responses={
            200: PRODUCT_DETAIL_RESPONSE,
            400: ERROR_400,
            404: ERROR_404,
        },
    )
    def put(self, request, pk):
        product, err = get_object_or_404_custom(Product, pk=pk)
        if err:
            return err
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(
        operation_summary="Partial update a product",
        operation_description="Partial update — only send fields you want to change.",
        request_body=ProductSerializer,
        responses={
            200: PRODUCT_DETAIL_RESPONSE,
            400: ERROR_400,
            404: ERROR_404,
        },
    )
    def patch(self, request, pk):
        product, err = get_object_or_404_custom(Product, pk=pk)
        if err:
            return err
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(
        operation_summary="Delete a product",
        operation_description="Deletes a product. Returns 204 with no body.",
        responses={
            204: NO_CONTENT_204,
            404: ERROR_404,
        },
    )
    def delete(self, request, pk):
        product, err = get_object_or_404_custom(Product, pk=pk)
        if err:
            return err
        product.delete()
        return Response(status=204)
