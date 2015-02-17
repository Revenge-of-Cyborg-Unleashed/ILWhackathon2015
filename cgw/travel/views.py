from django.shortcuts import render
from travel.forms import SearchForm
from django.http import HttpResponse

# Create your views here.

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect('/search/')
    else:
        form = SearchForm()
    return render(request, 'searchform.html', {'form': form})
