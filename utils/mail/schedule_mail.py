
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
import logging
from decouple import config
from app.models import ScheduledEmail


logger = logging.getLogger(__name__)

@shared_task
def send_scheduled_email(email_id):
    from django.core.mail import get_connection

    try:
        email = ScheduledEmail.objects.get(id=email_id)
        email_list = config("EMAIL_POOL").split(",")
        password_list = config("EMAIL_PASSWORD_POOL").split(",")

        if len(email_list) != len(password_list):
            logger.error("EMAIL_POOL and EMAIL_PASSWORD_POOL lengths do not match")
            return "Email credentials misconfigured"

   
        for from_email, password in zip(email_list, password_list):
            try:
                connection = get_connection(
                    backend='django.core.mail.backends.smtp.EmailBackend',
                    host=config("EMAIL_HOST"),
                    port=config("EMAIL_PORT", cast=int),
                    username=from_email,
                    password=password,
                    use_tls=config("EMAIL_USE_TLS", cast=bool),
                    use_ssl=config("EMAIL_USE_SSL", cast=bool, default=False),
                )

                if email.is_html:
                    text_content = strip_tags(email.body)
                    message = EmailMultiAlternatives(
                        subject=email.subject,
                        body=text_content,
                        from_email=from_email,
                        bcc=email.recipients,
                        connection=connection
                    )
                    message.attach_alternative(email.body, "text/html")
                else:
                    message = EmailMultiAlternatives(
                        subject=email.subject,
                        body=email.body,
                        from_email=from_email,
                        bcc=email.recipients,
                        connection=connection
                    )

                attachments = email.attachments.all()
                logger.info(f"Attempting to attach {attachments.count()} files")

                for attachment in attachments:
                    try:
                        if attachment.file:
                            with attachment.file.open('rb') as file:
                                message.attach(
                                    filename=attachment.name,
                                    content=file.read(),
                                    mimetype=attachment.content_type
                                )
                            logger.info(f"Attached file: {attachment.name}")
                        else:
                            logger.warning(f"No file found for attachment: {attachment.name}")
                    except Exception as attach_error:
                        logger.error(f"Failed to attach file {attachment.name}: {str(attach_error)}")

                message.send()
                email.status = 'sent'
                email.save()
                logger.info(f"Email {email_id} sent successfully using {from_email}")
                return f"Email {email_id} sent successfully"
            except Exception as e:
                logger.warning(f"Sending failed using {from_email}: {str(e)}")
                continue 

        logger.error(f"All email accounts failed to send email {email_id}")
        email.status = 'failed'
        email.save()
        return f"All email accounts failed to send email {email_id}"

    except ScheduledEmail.DoesNotExist:
        logger.error(f"Email {email_id} not found")
        return f"Email {email_id} not found"
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return f"Unexpected error: {str(e)}"
