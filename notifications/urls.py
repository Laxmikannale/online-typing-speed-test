# notifications/urls.py
from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # List all notifications
    path('', views.notification_list, name='list'),

    # Mark a single notification as read
    path('mark/<int:pk>/', views.mark_as_read, name='read'),

    # Mark all notifications as read
    path('mark_all/', views.mark_all_read, name='read_all'),

    # Send a new notification (admin/staff only)
    path('send/', views.send_notification, name='send'),
]
