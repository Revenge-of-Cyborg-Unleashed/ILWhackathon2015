from django.shortcuts import render
from travel.forms import SearchForm
from django.http import HttpResponse
from django.template import Context
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from travel.models import Group, Person, Quote, Flight

# Create your views here.

@csrf_protect
def search(request):
    csrfContext = RequestContext(request)
    return render_to_response('search.html',csrfContext)


def polltable(request):
    return render(request, "polltable.html")


def pollview(request,group_salt):
    group = Group.objects.get(salt=group_salt)
    people = Person.objects.filter(group_id=group)
    quotes = Quote.objects.filter(group_id=group)
    flights = []
    for q in quotes:
        flights.append(Flight.objects.filter(quote_id=q))

    print(group)
    print(people)
    print(quotes)
    print(flights)
    return render(request, 'polltable.html', {'name':people,'flights':quotes})


def submit(request):
    dict = request.POST
    print(dict.keys())
    return HttpResponse("hello")
