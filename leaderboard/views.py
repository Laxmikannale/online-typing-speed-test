from django.shortcuts import render
from django.utils.timezone import now, timedelta
from django.contrib.auth.decorators import login_required
from typingtest.models import Performance


@login_required
def leaderboard_view(request):
    """
    Leaderboard view:
    - Filters: today / week / all
    - Difficulty: easy / medium / hard / all
    - Shows top 10 performers (best WPM).
    """

    # --- Filters from query params ---
    time_filter = request.GET.get("time", "all")       # today / week / all
    difficulty_filter = request.GET.get("difficulty", "all")  # easy / medium / hard / all

    # --- Base Query ---
    performances = Performance.objects.all()

    # Apply difficulty filter
    if difficulty_filter.lower() != "all":
        performances = performances.filter(difficulty__iexact=difficulty_filter)

    # Apply time filter
    if time_filter == "today":
        performances = performances.filter(date__date=now().date())
    elif time_filter == "week":
        week_ago = now() - timedelta(days=7)
        performances = performances.filter(date__gte=week_ago)

    # --- Get each user’s best performance (highest WPM) ---
    best_performances = []
    user_ids = performances.values_list("user", flat=True).distinct()

    for user_id in user_ids:
        best_perf = performances.filter(user_id=user_id).order_by("-wpm").first()
        if best_perf:
            best_performances.append(best_perf)

    # Sort by WPM (descending) and take Top 10
    best_performances = sorted(best_performances, key=lambda x: x.wpm, reverse=True)[:10]

    # --- Chart Data (Top 5 users only) ---
    chart_labels = [perf.user.username for perf in best_performances[:5]]
    chart_wpm = [perf.wpm for perf in best_performances[:5]]
    chart_accuracy = [perf.accuracy for perf in best_performances[:5]]

    # --- Debugging (check terminal logs) ---
    print("🔥 Total Performances in DB:", Performance.objects.count())
    print("🔥 After filtering:", performances.count())
    print("🔥 Leaderboard:", [f"{p.user.username} - {p.wpm} WPM" for p in best_performances])

    # --- Context ---
    context = {
        "top_scores": best_performances,
        "time_filter": time_filter,
        "difficulty_filter": difficulty_filter,
        "chart_labels": chart_labels,
        "chart_wpm": chart_wpm,
        "chart_accuracy": chart_accuracy,
    }

    return render(request, "leaderboard.html", context)
