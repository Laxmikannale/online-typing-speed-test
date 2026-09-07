from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Notification
from .forms import NotificationForm


# ✅ List all notifications for logged-in user
@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications
    })


# ✅ Mark a single notification as read
@login_required
def mark_as_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect('notifications:list')


# ✅ Mark all notifications as read
@login_required
def mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('notifications:list')


# ✅ Admin/Staff: send a new notification
@user_passes_test(lambda u: u.is_staff)
def send_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            send_to_all = form.cleaned_data.pop('send_to_all', False)
            notif = form.save(commit=False)

            if send_to_all:
                # Send same notification to all users
                users = User.objects.all()
                for user in users:
                    Notification.objects.create(user=user, message=notif.message)
            else:
                notif.save()

            return redirect('notifications:list')
    else:
        form = NotificationForm()

    return render(request, 'notifications/send_notification.html', {'form': form})
