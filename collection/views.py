from django.shortcuts import render
from .models import CollectionEntry
from django.contrib.auth.decorators import login_required

def collected_items(request):
    items = CollectionEntry.objects.all()
    return render(request, 'collection/collected_items.html', {'items': items})
