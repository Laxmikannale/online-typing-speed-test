from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# ------------------------
# Register View
# ------------------------
def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # Password match check
        if password != confirm_password:
            messages.error(request, "❌ Passwords do not match!")
            return redirect('register')

        # Username exists check
        if User.objects.filter(username=username).exists():
            messages.error(request, "⚠ Username already exists!")
            return redirect('register')

        # Email exists check
        if User.objects.filter(email=email).exists():
            messages.error(request, "⚠ Email already registered!")
            return redirect('register')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, "✅ Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'accounts/register.html')

# ------------------------
# Login View
# ------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "✅ Successfully logged in!")

            return redirect('home')
        else:
            messages.error(request, "❌ Invalid username or password")
            return redirect('login')

    return render(request, 'accounts/login.html')

# ------------------------
# Logout View
# ------------------------
def logout_view(request):
    logout(request)
    messages.info(request, "👋 You have been logged out.")
    return redirect('home')
