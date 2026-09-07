from django.db import models
from django.contrib.auth.models import User


class Paragraph(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    text = models.TextField(help_text="The paragraph text for typing test")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")  # store minutes, front-end converts to seconds
    created_at = models.DateTimeField(auto_now_add=True)

    def short_preview(self, length=50):
        """Return a shortened preview of the text without cutting words."""
        if len(self.text) <= length:
            return self.text
        cutoff = self.text.rfind(' ', 0, length)
        return self.text[:cutoff] + "..."

    def __str__(self):
        return f"{self.get_difficulty_display()} - {self.duration} min | {self.short_preview()}"


class Performance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wpm = models.FloatField(help_text="Words per minute")
    accuracy = models.FloatField(help_text="Typing accuracy in percentage")
    errors = models.PositiveIntegerField(default=0, help_text="Number of typing errors")  # NEW FIELD
    difficulty = models.CharField(max_length=10, choices=Paragraph.DIFFICULTY_CHOICES)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']  # Always newest first

    def __str__(self):
        return f"{self.user.username} | {self.wpm:.2f} WPM | {self.accuracy:.2f}% | Errors: {self.errors}"
