from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings

def index(request):
    if request.is_mobile:
        return render_to_response('mobile/index.html', {"settings": settings})    
    return render_to_response('cash/index.html', {"settings": settings})
