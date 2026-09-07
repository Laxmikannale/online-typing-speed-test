from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import random

from .models import Performance, Paragraph


# 🏠 Home Page
def home(request):
    return render(request, 'typingtest/home.html')


# 🔑 Custom Login View — logs out old user before logging in a new one
def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # ✅ Always log out any existing user first
        if request.user.is_authenticated:
            logout(request)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # ✅ Success message after login
            messages.success(request, "✅ Successfully logged in!")
            return redirect('home')  # Redirect to homepage
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'registration/login.html')  # Your login template


# 📝 Start Typing Test Page
@login_required
def start_test(request):
    return render(request, 'typingtest/start_test.html')


# 📜 API to Get a Random Paragraph
@login_required
def get_paragraph(request):
    difficulty = request.GET.get('difficulty', 'easy').strip().lower()

    try:
        duration_raw = int(request.GET.get('duration', 60))
    except ValueError:
        return JsonResponse({"error": "Invalid duration"}, status=400)

    # Convert to minutes
    duration_minutes = duration_raw // 60 if duration_raw > 5 else duration_raw

    # Filter paragraphs
    paragraphs = Paragraph.objects.filter(
        difficulty=difficulty,
        duration=duration_minutes
    )

    if not paragraphs.exists():
        return JsonResponse({"text": None})

    paragraph = random.choice(list(paragraphs))
    return JsonResponse({"text": paragraph.text})


# 💾 Save Performance
@login_required
@csrf_exempt
def save_performance(request):
    if request.method == 'POST':
        try:
            # Handle JSON and Form Data
            if request.content_type == "application/json":
                data = json.loads(request.body)
            else:
                data = request.POST

            wpm = float(data.get('wpm', 0))
            accuracy = float(data.get('accuracy', 0))
            errors = int(data.get('errors', 0))
            difficulty = data.get('difficulty', 'easy')
            duration = int(data.get('duration', 1))  # store in minutes

            # Save record
            Performance.objects.create(
                user=request.user,
                wpm=wpm,
                accuracy=accuracy,
                errors=errors,
                difficulty=difficulty,
                duration=duration
            )

            # Send optional email
            if request.user.email:
                try:
                    send_mail(
                        subject="Typing Test Completed 🎉",
                        message=(
                            f"Hi {request.user.username},\n\n"
                            f"Your Typing Test results:\n"
                            f"- WPM: {wpm}\n"
                            f"- Accuracy: {accuracy}%\n"
                            f"- Errors: {errors}\n"
                            f"- Difficulty: {difficulty.capitalize()}\n"
                            f"- Duration: {duration} minute(s)\n\n"
                            f"Keep practicing!"
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[request.user.email],
                        fail_silently=True,
                    )
                except Exception:
                    pass

            # Return JSON if AJAX
            if request.content_type == "application/json":
                return JsonResponse({
                    "status": "success",
                    "show_button": True,
                    "performance_url": "/performance/"
                })

            # Redirect to performance page after saving
            return redirect('performance_tracking')

        except Exception as e:
            if request.content_type == "application/json":
                return JsonResponse({"status": "error", "message": str(e)}, status=400)
            messages.error(request, f"Error saving performance: {e}")
            return redirect('home')

    return redirect('home')


# 📊 User's Performance Tracking
@login_required
def performance_tracking(request):
    performances = Performance.objects.filter(user=request.user).order_by('-date')
    return render(request, 'typingtest/performance.html', {
        'performances': performances
    })


# 🏆 Leaderboard
@login_required
def leaderboard_view(request):
    leaderboard = Performance.objects.order_by('-wpm', '-accuracy')[:10]
    return render(request, 'typingtest/leaderboard.html', {
        'leaderboard': leaderboard
    })


# 📧 Test Email Sending
def test_email(request):
    try:
        send_mail(
            subject="Test Email from Django",
            message="Hello! This is a test email to verify your email settings.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["your_email@gmail.com"],  # Change to your email
            fail_silently=False,
        )
        return HttpResponse("✅ Test email sent successfully!")
    except Exception as e:
        return HttpResponse(f"❌ Failed to send email: {e}")
