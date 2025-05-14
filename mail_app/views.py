# email_scheduler/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.conf import settings
from django.core.files.base import ContentFile
import base64
import json
from datetime import datetime
import uuid

from app.models import ScheduledEmail, EmailAttachment
from app.serializers import ScheduledEmailSerializer
from utils.mail.schedule_mail import send_scheduled_email

class SendEmailView(APIView):
    def post(self, request):
        try:
            data = request.data
            
            email_data = {
                'subject': data.get('subject'),
                'body': data.get('body'),
                'is_html': data.get('useHtml', False),
                'recipients': data.get('recipients', []),
                'scheduled_at': data.get('scheduledAt')
            }
            
      
            serializer = ScheduledEmailSerializer(data=email_data)
            if not serializer.is_valid():
                return Response(
                    {'message': 'Invalid data', 'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            email = serializer.save()
            

            
            attachments = data.get('attachments', [])
            
            for attachment_data in attachments:
                print('content not in attacment')
                print(attachment_data)
                if 'content' in attachment_data:
                    print('content is in attacment')
                    file_content = base64.b64decode(attachment_data['content'].split(',')[1])
                    
                    EmailAttachment.objects.create(
                        email=email,
                        name=attachment_data.get('name', ''),
                        file=ContentFile(file_content, name=attachment_data.get('name', '')), 
                        size=len(file_content),
                        content_type=attachment_data.get('type', 'application/octet-stream')
                    )
            

            if email.scheduled_at and email.scheduled_at > timezone.now():
            
                task = send_scheduled_email.apply_async(
                    args=[email.id],
                    eta=email.scheduled_at
                )
                email.task_id = task.id
                email.save()
                message = f"Email scheduled for {email.scheduled_at}"
            else:
                # Send immediately
                task = send_scheduled_email.apply_async(args=[email.id])
                email.task_id = task.id
                email.save()
                message = "Email scheduled for immediate delivery"
            
            return Response({
                'success': True,
                'message': message,
                'email_id': email.id
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(e)
            return Response({
                'success': False,
                'message': f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)