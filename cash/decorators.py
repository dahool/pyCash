try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.
from django.utils.decorators import available_attrs
from django.http import HttpResponse
from django.conf import settings
from jsonui.response import JSONResponse

def json_response(view_func):
    def _wrapped_view(request, *args, **kwargs):

        context = view_func(request, *args, **kwargs)

        if isinstance(context, HttpResponse):
            return context        
        
        try:
            cook = context.pop('cookjar',None)
        except:
            cook = None

        response = JSONResponse(request, context)

        if isinstance(response, HttpResponse):
            if cook:
                for k,v in cook.iteritems():
                    if v is None:
                        response.delete_cookie(str(k))
                    else:
                        response.set_cookie(str(k), str(v), getattr(settings, 'COMMON_COOKIE_AGE', None))
        return response
    return wraps(view_func, assigned=available_attrs(view_func))(_wrapped_view)
