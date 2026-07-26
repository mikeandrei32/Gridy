from backend.config.urls import urlpatterns
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from gridy_communications.views import AnnouncementViewSet, ActivityScheduleViewSet

router = DefaultRouter()
router.register(r'announcements', AnnouncementViewSet, basename='announcement')
router.register(r'activities', ActivityScheduleViewSet, basename='activity')

urlpatterns = [
    path('', include(router.urls)),
]