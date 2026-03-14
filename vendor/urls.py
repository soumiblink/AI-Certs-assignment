from django.urls import path
from .views import VendorListCreateView, VendorDetailView
from .full_structure_view import VendorFullStructureView

urlpatterns = [
    path('', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('<int:pk>/', VendorDetailView.as_view(), name='vendor-detail'),
    path('<int:vendor_id>/full-structure/', VendorFullStructureView.as_view(), name='vendor-full-structure'),
]
