from django.urls import path
from .views import ProductCourseMappingListCreateView, ProductCourseMappingDetailView

urlpatterns = [
    path('', ProductCourseMappingListCreateView.as_view(), name='product-course-mapping-list-create'),
    path('<int:pk>/', ProductCourseMappingDetailView.as_view(), name='product-course-mapping-detail'),
]
