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
from datetime import datetime

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
    print (dict['inputDeparture'])
    destination_place = dict['inputArrival']
    print (dict['inputArrival'])
    date = dict['depart']
    #converted_date = date[6:] + "-" + date[3:5] + "-" + date[:2]
    converted_date = date.replace("/", "-")
    outbound_partial_date = converted_date
    print (converted_date)
    date = dict['returndate']
    #converted_date = date[6:] + "-" + date[3:5] + "-" + date[:2]
    converted_date = date.replace("/", "-")
    inbound_partial_date = converted_date
    group_name = dict['groupName']
    print (dict['groupName'])
    names_with_emails = dict['listOfUsers']
    split_names = names_with_emails.split('\n')
    tuple_array = []
    for name_email in split_names:
        if name_email is not '':
            temp = name_email.split(", ")
            print (temp)
            name = temp[0]
            print (name)
            email = temp[1]
            email = email.replace('\r','')
            tuple_array.append((name,email))
            print (tuple)
    names_emails = tuple_array
   # print ('P')
   # print (dict['listOfUsers'])
   # print ('P')
   # print (type(names_emails))
    object = saveQuery(origin_place, destination_place, outbound_partial_date, inbound_partial_date, group_name, names_emails)
    salt = object.doQuery()
    return HttpRequest.path("group/"+salt+"/"), 
    #return HttpResponse("hello")
