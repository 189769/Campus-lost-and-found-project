from django import forms
from .models import LostItem, FoundReport

class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostItem
        fields = ['title', 'description', 'category', 'location', 'date_lost', 'image']

class FoundReportForm(forms.ModelForm):
    class Meta:
        model = FoundReport
        fields = ['message']
