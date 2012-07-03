from django.contrib.auth.backends import ModelBackend
from cash.models import AuthToken, TokenUsage

class RemoteTokenBackend(ModelBackend):
    """
    This backend is to be used in conjunction with the ``RemoteTokenMiddleware``
    found in the middleware module of this package, and is used when the server
    is handling authentication outside of Django.
    """

    def authenticate(self, remote_token, remote_user, remote_ip):
        
        if not remote_token or not remote_user:
            return

        user = None
        try:
            authtoken = AuthToken.objects.get(token=remote_token, user__username=remote_user)
            user = authtoken.user

            obj, created = TokenUsage.objects.get_or_create(token=authtoken, ip=remote_ip)
            if not created:
                obj.save() # if the object already exists, we force a save to update the last access date
        except AuthToken.DoesNotExist:
            pass
        return user