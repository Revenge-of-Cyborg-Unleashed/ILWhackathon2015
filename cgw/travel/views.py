from django.shortcuts import render
from travel.forms import SearchForm
from django.http import HttpResponse
from django.template import Context
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from travel.models import Group, Person, Quote, Flight
from travel.fetch_query import saveQuery

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
    return render(request, 'polltable.html', {'people':people,'flights':quotes})

def submit(request):
    dict = request.POST
    origin_place = dict['inputDeparture']
    destination_place = dict['inputArrival']
    print (dict['inputArrival'])
    outbound_partial_date = dict['depart']
    print (dict['depart'])
    inbound_partial_date = dict['returndate']
    print (dict['returndate'])
    group_name = dict['groupName']
    print (dict['groupName'])
    names_emails = dict['listOfUsers']
    print (dict['listOfUsers'])
    object = saveQuery(origin_place, destination_place, outbound_partial_date, inbound_partial_date, group_name, names_emails)
    salt = object.doQuery()
    #return HttpRequest.path("group/"+salt+"/"), 
    return HttpResponse("hello")
