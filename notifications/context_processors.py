def header_notifications(request):
    if not request.user.is_authenticated:
        return {}
    qs = request.user.notifications.all()[:5]
    unread = request.user.notifications.filter(is_read=False).count()
    return {
        'header_notifications': qs,
        'notifications_unread_count': unread,
    }
