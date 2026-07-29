from rest_framework import serializers
from .models import DocumentRequest, QueueTicket

class DocumentRequestSerializer(serializers.ModelSerializer):
    request_id = serializers.IntegerField(source='id', read_only=True)
    requester_name = serializers.SerializerMethodField()
    
    class Meta:
        model = DocumentRequest
        fields = [
            'request_id',
            'requester_name',
            'document_type',
            'urgency_tag',
            'status',
            'admin_notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_requester_name(self, obj):
        user = obj.user
        return getattr(user.profile, 'full_name', user.username) if hasattr(user,'profile') else user.username

class QueueTicketSerializer(serializers.ModelSerializer):
    ticket_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = QueueTicket
        fields = [
            'ticket_id',
            'ticket_number',
            'service_type',
            'status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['status', 'ticket_number', 'created_at', 'updated_at']
