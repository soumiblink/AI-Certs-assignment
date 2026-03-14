from django.urls import path
from .views import CertificationListCreateView, CertificationDetailView

urlpatterns = [
    path('', CertificationListCreateView.as_view(), name='certification-list-create'),
    path('<int:pk>/', CertificationDetailView.as_view(), name='certification-detail'),
]
