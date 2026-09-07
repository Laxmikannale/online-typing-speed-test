from django.db import models
from django.contrib.auth.models import User

class LeaderboardEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wpm = models.FloatField()  # Words Per Minute
    accuracy = models.FloatField()  # Accuracy in %
    test_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-wpm']  # Highest WPM first

    def __str__(self):
        return f"{self.user.username} - {self.wpm} WPM - {self.accuracy}%"
