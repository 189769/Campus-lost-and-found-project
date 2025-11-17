# collection/models.py
from django.db import models
from django.contrib.auth.models import User
from lost_items.models import LostItem

class CollectionEntry(models.Model):
    item = models.OneToOneField(LostItem, on_delete=models.CASCADE)
    collected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    collected_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Collected: {self.item.title}"