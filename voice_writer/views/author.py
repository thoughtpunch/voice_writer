from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from voice_writer.models.author import Author
from voice_writer.forms.author import AuthorForm


@login_required
def author_profile(request):
    author = Author.objects.filter(user=request.user).first()
    return render(request, 'voice_writer/author/author.html', {'author': author})


@login_required
def update_author(request):
    author = Author.objects.get(user=request.user)

    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES, instance=author)
        if form.is_valid():
            form.save()
            return render(request, 'voice_writer/author/author.html', {'author': author})
    else:
        form = AuthorForm(instance=author)

    return render(request, 'voice_writer/author/author.html', {'author': author})