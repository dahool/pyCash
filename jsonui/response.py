# -*- coding: utf-8 -*-

from utils import serialize_to_json
from django.http import HttpResponseForbidden, HttpResponse
from django.utils.encoding import force_unicode

JSONP_CALLBACK = 'jqback'

class JSONResponse(HttpResponse):
    """ JSON response class """
    def __init__(self, request, content='',json_opts={},mimetype="application/json",*args,**kwargs):
        """
        This returns a object that we send as json content using 
        utils.serialize_to_json, that is a wrapper to simplejson.dumps
        method using a custom class to handle models and querysets. Put your
        options to serialize_to_json in json_opts, other options are used by
        response.
        """
        if not isinstance(content, basestring):
            if content:
                content = serialize_to_json(content,**json_opts)
            else:
                content = serialize_to_json([],**json_opts)
        mimetype = "text/javascript";
        if (JSONP_CALLBACK in request.REQUEST):
            content = '%s(%s)' % (request.REQUEST[JSONP_CALLBACK], serialize_to_json(content));
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)

