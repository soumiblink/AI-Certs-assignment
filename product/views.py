from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.utils import get_object_or_404_custom, success_response, error_response
from .models import Product
from .serializers import ProductSerializer

vendor_id_param = openapi.Parameter('vendor_id', openapi.IN_QUERY, description="Filter by vendor ID", type=openapi.TYPE_INTEGER)


class ProductListCreateView(APIView):

    @swagger_auto_schema(
        operation_summary="List all products",
        manual_parameters=[vendor_id_param],
        responses={200: ProductSerializer(many=True)},
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
        request_body=ProductSerializer,
        responses={201: ProductSerializer},
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, status_code=201)
        return error_response(serializer.errors)


class ProductDetailView(APIView):

    @swagger_auto_schema(operation_summary="Retrieve a product", responses={200: ProductSerializer})
    def get(self, request, pk):
        product, err = get_object_or_404_custom(Product, pk=pk)
        if err:
            return err
        return success_response(ProductSerializer(product).data)

    @swagger_auto_schema(operation_summary="Update a product", request_body=ProductSerializer, responses={200: ProductSerializer})
    def put(self, request, pk):
        product, err = get_object_or_404_custom(Product, pk=pk)
        if err:
            return err
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(operation_summary="Partial update a product", request_body=ProductSerializer, responses={200: ProductSerializer})
    def patch(self, request, pk):
        product, err = get_object_or_404_custom(Product, pk=pk)
        if err:
            return err
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)
        return error_response(serializer.errors)

    @swagger_auto_schema(operation_summary="Delete a product", responses={204: "No Content"})
    def delete(self, request, pk):
        product, err = get_object_or_404_custom(Product, pk=pk)
        if err:
            return err
        product.delete()
        return success_response({"message": "Product deleted successfully."}, status_code=204)
