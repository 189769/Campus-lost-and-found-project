from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import LostItem, FoundReport
from .forms import LostItemForm, FoundReportForm
from collection.models import CollectionEntry
from django.shortcuts import render
from .models import LostItem
from django.contrib.auth.decorators import login_required

from django.shortcuts import render

def lost_items_list(request):
    return render(request, 'lost_items_list.html')

def add_lost_item(request):
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_lost_items')  # Redirect to the page that lists all items
    else:
        form = LostItemForm()

    return render(request, 'lost_items/add_lost_item.html', {'form': form})

def view_lost_items(request):
    items = LostItem.objects.all()
    return render(request, 'lost_items/view_lost_items.html', {'items': items})


def home(request):
    return render(request, 'base.html')


def item_list(request):
    items = LostItem.objects.exclude(status='collected').order_by('-date_reported')
    return render(request, 'lost_items/item_list.html', {'items': items})

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

@login_required
def post_lost_item(request):
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES)
        if form.is_valid():
            lost = form.save(commit=False)
            lost.reporter = request.user
            lost.save()
            return redirect('lost_items:item_detail', pk=lost.pk)
    else:
        form = LostItemForm()
    return render(request, 'lost_items/post_lost_item.html', {'form': form})

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
            # optionally notify the reporter via email or notification in-app
            return redirect('lost_items:item_detail', pk=pk)
    return redirect('lost_items:item_detail', pk=pk)

@login_required
def confirm_found(request, report_pk):
    # reporter or admin can confirm the found report
    report = get_object_or_404(FoundReport, pk=report_pk)
    item = report.item
    # confirm and set item status to found
    report.confirmed = True
    report.save()
    item.status = 'found'
    item.save()
    # optionally notify finder
    return redirect('lost_items:item_detail', pk=item.pk)

@login_required
def collect_item(request, pk):
    # Called when the owner collects the item (or admin marks collected)
    item = get_object_or_404(LostItem, pk=pk)
    # create collection entry and set status
    from collection.models import CollectionEntry
    entry = CollectionEntry.objects.create(item=item, collected_by=request.user)
    item.status = 'collected'
    item.save()
    return redirect('collections:entry_detail', pk=entry.pk)
