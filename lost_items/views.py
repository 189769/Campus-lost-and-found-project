from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import LostItem, FoundReport
from .forms import LostItemForm, FoundReportForm
from collection.models import CollectionEntry

def home(request):
    return render(request, 'home.html')

def view_lost_items(request):
    items = LostItem.objects.all().order_by('-date_reported')
    return render(request, 'lost_items/view_lost_items.html', {'items': items})

@login_required
def add_lost_item(request):
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            lost_item = form.save(commit=False)
            lost_item.reporter = request.user   # attach user
            lost_item.save()
            return redirect('view_lost_items')
    else:
        form = LostItemForm()
    return render(request, 'lost_items/add_lost_item.html', {'form': form})

def search_items(request):
    q = request.GET.get('q', '')
    items = LostItem.objects.exclude(status='collected')

    if q:
        items = items.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(location__icontains=q) |
            Q(category__icontains=q)
        )
    return render(request, 'lost_items/search_results.html', {'items': items, 'q': q})

def item_detail(request, pk):
    item = get_object_or_404(LostItem, pk=pk)
    found_form = FoundReportForm()
    return render(request, 'lost_items/item_detail.html', {'item': item, 'found_form': found_form})

@login_required
def report_found(request, pk):
    item = get_object_or_404(LostItem, pk=pk)
    if request.method == 'POST':
        form = FoundReportForm(request.POST)
        if form.is_valid():
            fr = form.save(commit=False)
            fr.item = item
            fr.finder = request.user
            fr.save()
            return redirect('item_detail', pk=pk)
    return redirect('item_detail', pk=pk)

@login_required
def confirm_found(request, report_pk):
    report = get_object_or_404(FoundReport, pk=report_pk)
    item = report.item
    report.confirmed = True
    report.save()
    item.status = 'found'
    item.save()
    return redirect('item_detail', pk=item.pk)

@login_required
def collect_item(request, pk):
    item = get_object_or_404(LostItem, pk=pk)
    entry = CollectionEntry.objects.create(item=item, collected_by=request.user)
    item.status = 'collected'
    item.save()
    return redirect('collections:entry_detail', pk=entry.pk)
