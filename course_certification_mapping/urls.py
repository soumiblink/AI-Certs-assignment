from django.urls import path
from .views import CourseCertificationMappingListCreateView, CourseCertificationMappingDetailView

urlpatterns = [
    path('', CourseCertificationMappingListCreateView.as_view(), name='course-certification-mapping-list-create'),
    path('<int:pk>/', CourseCertificationMappingDetailView.as_view(), name='course-certification-mapping-detail'),
]
