import threading
from django.core.mail import EmailMultiAlternatives, get_connection
from decouple import config

EMAIL_POOL = config('EMAIL_POOL').split(',')  
PASSWORD_POOL = config('EMAIL_PASSWORD_POOL').split(',')  


class EmailThread(threading.Thread):
    def __init__(self, subject, message, recipient_list, html):
        self.subject = subject
        self.message = message
        self.recipient_list = recipient_list
        self.html = html
        threading.Thread.__init__(self)

    def run(self):
        for email, password in zip(EMAIL_POOL, PASSWORD_POOL):
            try:
                
                connection = get_connection(
                    username=email,
                    password=password,
                    fail_silently=False,
                )

                msg = EmailMultiAlternatives(
                    subject=self.subject,
                    body=self.message,
                    from_email=email,
                    to=[], 
                    bcc=self.recipient_list,
                    connection=connection
                )

                if self.html:
                    msg.attach_alternative(self.html, "text/html")

                msg.send()
                
                break

            except Exception as e:
                continue


def send(subject, message, recipient_list, html):
    EmailThread(subject, message, recipient_list, html).start()
