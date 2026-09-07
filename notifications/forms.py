from django import forms
from .models import Notification

class NotificationForm(forms.ModelForm):
    # Extra checkbox for admin: send to all users
    send_to_all = forms.BooleanField(required=False, initial=False, label="Send to all users")

    class Meta:
        model = Notification
        fields = ['user', 'message']
