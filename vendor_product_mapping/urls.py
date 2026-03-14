from django.urls import path
from .views import VendorProductMappingListCreateView, VendorProductMappingDetailView

urlpatterns = [
    path('', VendorProductMappingListCreateView.as_view(), name='vendor-product-mapping-list-create'),
    path('<int:pk>/', VendorProductMappingDetailView.as_view(), name='vendor-product-mapping-detail'),
]
