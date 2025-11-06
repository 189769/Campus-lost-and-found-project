from django.conf import settings
from django.db import models

class LostItem(models.Model):
    STATUS_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
        ('collected', 'Collected'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)  # optional
    location = models.CharField(max_length=200, blank=True)
    date_reported = models.DateTimeField(auto_now_add=True)
    date_lost = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='lost_items/', blank=True, null=True)
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='lost')

    def __str__(self):
        return f"{self.title} ({self.status})"

class FoundReport(models.Model):
    item = models.ForeignKey(LostItem, on_delete=models.CASCADE, related_name='found_reports')
    finder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    date_found = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)  # reporter or admin can confirm

    def __str__(self):
        return f"FoundReport for {self.item.title} by {self.finder.username}"
