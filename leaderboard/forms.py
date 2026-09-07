from django import forms
from .models import Notification

class NotificationForm(forms.ModelForm):
    send_to_all = forms.BooleanField(required=False, help_text="Send to all users instead of one.")

    class Meta:
        model = Notification
        fields = ['user', 'message']
