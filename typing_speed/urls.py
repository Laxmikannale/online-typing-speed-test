from django.contrib import admin
from django.urls import path, include
from typingtest import views as typing_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home & Typing Test routes
    path('', include('typingtest.urls')),

    # Performance tracking
    path('performance/', typing_views.performance_tracking, name='performance_tracking'),

    # Accounts (login, register, logout)
    path('accounts/', include('accounts.urls')),

    # Leaderboard module
    path('leaderboard/', include('leaderboard.urls')),

    path('notifications/', include('notifications.urls')),

]
