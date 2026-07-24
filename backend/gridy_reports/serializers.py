from rest_framework import serializers
from .models import IssueReport

class IssueReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueReport
        fields = '__all__'
        read_only_fields = ['reporter']