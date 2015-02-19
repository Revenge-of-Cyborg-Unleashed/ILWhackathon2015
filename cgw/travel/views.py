from django.shortcuts import render
from travel.forms import SearchForm
from django.http import HttpResponse
from django.template import Context
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext

# Create your views here.

@csrf_protect
def search(request):
    csrfContext = RequestContext(request)
    return render_to_response('search.html',csrfContext)


def polltable(request):
    return render(request, "polltable.html")


def pollview(request,group_salt):
    people = [{'name':"bob", "email":"bob@bob.com"},{'name':"John", "email":"john@bob.com"}]
    flights = ["1","2","3","4"]
    c = {'people':people,'flights':flights}
    return render(request, 'polltable.html', {'people':people,'flights':flights})


def submit(request):
    dict = request.POST
    print(dict.keys())
    return HttpResponse("hello")
