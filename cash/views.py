from django.http import HttpResponse
from django.shortcuts import render_to_response
from pyCash import settings

def index(request):
    return render_to_response('cash/index.html', {"settings": settings})

#def detail(request, poll_id):
#    return HttpResponse("You're looking at poll %s." % poll_id)

