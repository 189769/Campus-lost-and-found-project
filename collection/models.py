from django.conf import settings
from django.db import models
from lost_items.models import LostItem

class CollectionEntry(models.Model):
    item = models.OneToOneField(LostItem, on_delete=models.CASCADE, related_name='collection_entry')
    collected_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    collected_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Collected: {self.item.title}"
