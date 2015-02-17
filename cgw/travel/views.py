from django.shortcuts import render
from travel.forms import SearchForm
from django.http import HttpResponse
from django.template import Context

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


def polltable(request):
    return render(request, "polltable.html")


def pollview(request,group_salt):
    people = [{'fname':"bob", "lnmae":"Bobby","email":"bob@bob.com"},{'fname':"John", "lnmae":"Bobby","email":"john@bob.com"}]
    flights = ["1","2","3","4"]
    c = {'people':people,'flights':flights}
    return render(request, 'polltable.html', {'people':people,'flights':flights})
