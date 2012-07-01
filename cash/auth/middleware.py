from django.contrib import auth
from django.core.exceptions import ImproperlyConfigured
from cash.models import AuthToken, TokenUsage

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
    token_user = "REMOTE_USER"

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
            token = request.META[self.token_header]
            username = request.META[self.token_user]
        except KeyError:
            # If specified header doesn't exist then return (leaving
            # request.user set to AnonymousUser by the
            # AuthenticationMiddleware).
            return
        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated():
            if request.user.username == username:
                return
        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        try:
            authtoken = AuthToken.objects.get(token=token, user__username=username)
            # User is valid.  Set request.user and persist user in the session
            # by logging the user in.
            auth.login(request, authtoken.user)
            obj, created = TokenUsage.objects.get_or_create(token=authtoken, ip=get_client_ip(request))
            if not created:
                obj.save() # if the object already exists, we force a save to update the last access date
        except AuthToken.DoesNotExist:
            # if passed data is invalid and there is an authenticated session,
            # we destroy the current logged session
            auth.logout(request)
