from django.shortcuts import render, redirect, get_object_or_404
from .models import Status
from django.http import HttpResponse
from django.views import View
from .forms import StatusForm

class StatusListView(View):
    def get(self, request):
        statuses = Status.objects.all()
        return render(request, 'statuses/status_list.html', {'statuses': statuses})

class StatusCreateView(View):
    def get(self, request):
        form = StatusForm()
        return render(request, 'statuses/status_form.html', {'form': form})

    def post(self, request):
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('statuses:list')
        return render(request, 'statuses/status_form.html', {'form': form})

class StatusUpdateView(View):
    def get(self, request, pk):
        status = get_object_or_404(Status, pk=pk)
        form = StatusForm(instance=status)
        return render(request, 'statuses/status_form.html', {'form': form})

    def post(self, request, pk):
        status = get_object_or_404(Status, pk=pk)
        form = StatusForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            return redirect('statuses:list')
        return render(request, 'statuses/status_form.html', {'form': form})

class StatusDeleteView(View):
    def get(self, request, pk):
        status = get_object_or_404(Status, pk=pk)
        return render(request, 'statuses/status_confirm_delete.html', {'status': status})

    def post(self, request, pk):
        status = get_object_or_404(Status, pk=pk)
        status.delete()
        return redirect('statuses:list')

