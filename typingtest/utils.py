# typingtest/utils.py
from django.core.mail import send_mail
from django.conf import settings

def send_notification_email(subject, message, recipient_list):
    """
    Sends an email using Django's send_mail.
    recipient_list must be a list, e.g. ["user@example.com"].
    """
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )
