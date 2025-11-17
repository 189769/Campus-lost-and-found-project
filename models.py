# lost_items/models.py
from django.db import models
from django.contrib.auth.models import User

class LostItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date_lost = models.DateField()
    image = models.ImageField(upload_to="lost_items/", blank=True, null=True)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)

    def _str_(self):
        return self.title