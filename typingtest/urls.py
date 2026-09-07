from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # ✅ Home page
    path('start/', views.start_test, name='start_test'),
    path('save-performance/', views.save_performance, name='save_performance'),
    path('performance/', views.performance_tracking, name='performance_tracking'),
    path('leaderboard/', include("leaderboard.urls")),  # ✅ Leaderboard app
    path('test-email/', views.test_email, name='test_email'),
    path('get_paragraph/', views.get_paragraph, name='get_paragraph'),
    path('login/', views.custom_login_view, name='login'),
]
