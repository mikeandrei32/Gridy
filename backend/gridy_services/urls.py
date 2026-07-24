from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentRequestViewSet, QueueTicketViewSet

router = DefaultRouter()
router.register(r'document-requests', DocumentRequestViewSet, basename='document-request')
router.register(r'tickets', QueueTicketViewSet, basename='ticket')

urlpatterns = [
    path('', include(router.urls)),
]