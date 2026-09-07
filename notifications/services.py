from .models import Notification

def notify(user, message):
    return Notification.objects.create(user=user, message=message)

def notify_all(users, message):
    objs = [Notification(user=u, message=message) for u in users]
    return Notification.objects.bulk_create(objs)
