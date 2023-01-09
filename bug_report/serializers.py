from rest_framework import serializers
from .models import BugReport

class BugReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BugReport
        fields = ['id', 'page', 'description', 'created_at', 'user_id']
