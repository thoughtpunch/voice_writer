from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from voice_writer.models.manuscript import Manuscript


@login_required
def index(request):
    manuscripts = Manuscript.objects.filter(author=request.user)
    return render(request, 'voice_writer/manuscript/list.html', {'manuscripts': manuscripts})
