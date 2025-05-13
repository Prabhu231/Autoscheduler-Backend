from rest_framework import serializers
from .models import ScheduledEmail, EmailAttachment

class EmailAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAttachment
        fields = ['name', 'size', 'content_type']

class ScheduledEmailSerializer(serializers.ModelSerializer):
    attachments = EmailAttachmentSerializer(many=True, required=False)
    
    class Meta:
        model = ScheduledEmail
        fields = ['id', 'subject', 'body', 'is_html', 'recipients', 'scheduled_at', 'status', 'attachments']
        read_only_fields = ['id', 'status']
    
    def create(self, validated_data):
        attachments_data = validated_data.pop('attachments', [])
        scheduled_email = ScheduledEmail.objects.create(**validated_data)
        

        return scheduled_email