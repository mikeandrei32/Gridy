from rest_framework import serializers
from gridy_communications.models import Announcement, ActivitySchedule, FCMDevice

class FCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        fields = ['id', 'token', 'created_at']


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

