from rest_framework import viewsets, permissions
from gridy_auth.permissions import IsBarangayOfficial
from gridy_communications.models import Announcement, ActivitySchedule
from gridy_communications.serializers import AnnouncementSerializer, ActivityScheduleSerializer

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all().order_by('-is_pinned', '-created_at')
    serializer_class = AnnouncementSerializer

    # 1. Dynamically apply permissions based on actions
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Anyone logged in (Resident or Official) can read
            return [permissions.IsAuthenticated()]
        # Only officials can write (create, update, delete)
        return [IsBarangayOfficial]
    
    # 2. Auto-assign the creator when saving
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ActivityScheduleViewSet(viewsets.ModelViewSet):
    queryset = ActivitySchedule.objects.all().order_by('event_datetime', 'created_at')
    serializer_class = ActivityScheduleSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Anyone logged in (Resident or Official) can read
            return [permissions.IsAuthenticated()]
        # Only officials can write (create, update, delete)
        return [IsBarangayOfficial]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)