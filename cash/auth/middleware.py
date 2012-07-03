from django.contrib import auth
from django.core.exceptions import ImproperlyConfigured

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
    
class RemoteTokenMiddleware(object):
    """
    Middleware for utilizing Token based authentication.

    If request.user is not authenticated, then this middleware attempts to
    authenticate the username passed in the ``REMOTE_TOKEN`` request header.
    If authentication is successful, the user is automatically logged in to
    persist the user in the session.
    """

    token_header = "REMOTE_TOKEN"

    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")

        try:
            data = request.POST[self.token_header]
            username, token = data.split('-') 
        except:
            # If specified header doesn't exist then return (leaving
            # request.user set to AnonymousUser by the
            # AuthenticationMiddleware).
            return
        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        
        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        try:
            user = auth.authenticate(remote_token=token, remote_user=username, remote_ip=get_client_ip(request))
            if user:
                request.user = user
                auth.login(request, user)
            else:
                # if passed data is invalid and there is an authenticated session,
                # we destroy the current logged session
                auth.logout(request)
        except:
            pass