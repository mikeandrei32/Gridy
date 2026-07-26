from rest_framework import serializers
from gridy_communications.models import Announcement, ActivitySchedule

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'
        read_only_fields = ['created_by']


class ActivityScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivitySchedule
        fields = '__all__'
        read_only_fields = ['created_by']

