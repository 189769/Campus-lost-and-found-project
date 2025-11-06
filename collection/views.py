from django.shortcuts import render

def collected_items(request):
    return render(request, 'collection/collected_items.html')
