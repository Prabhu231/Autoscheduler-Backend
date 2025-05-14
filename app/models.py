from django.db import models
from django.core.validators import RegexValidator
from datetime import timezone

class User(models.Model):
    
    email = models.EmailField(unique=True, max_length=150)
    password = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[^A-Za-z0-9]).{8,}$',
                message="Password must be at least 8 characters long, with at least one uppercase letter, one lowercase letter, one number, and one special character."
            )
        ]
    )
    blacklist_token = models.CharField(max_length=200, default='')
    
    
class ScheduledEmail(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    )
    
    subject = models.CharField(max_length=255)
    body = models.TextField()
    is_html = models.BooleanField(default=False)
    recipients = models.JSONField() 
    scheduled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    task_id = models.CharField(max_length=50, null=True, blank=True) 
    
    def __str__(self):
        return f"{self.subject} - {self.status}"

class EmailAttachment(models.Model):
    email = models.ForeignKey(ScheduledEmail, related_name='attachments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='email_attachments/')
    size = models.IntegerField()
    content_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    

