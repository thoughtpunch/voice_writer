from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def load_summary(request):
    context = {
        'summary': "This is a dynamically loaded summary using HTMX."
    }
    return render(request, 'voice_writer/summary.html', context)


@login_required
def index(request):
    return render(request, 'voice_writer/index.html')
