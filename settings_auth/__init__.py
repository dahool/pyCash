from django.conf import settings
from django.contrib.auth.models import User

class SettingsAuthBackend:
    
    supports_anonymous_user = False
    
    def authenticate(self, username=None, password=None):
        if (username == getattr(settings,'ADMIN_LOGIN','admin') 
            and password ==  getattr(settings,'ADMIN_PWD','admin')):
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create(username=username,
                                           is_staff=True,
                                           is_superuser=True)
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
    def has_perm(self, user_obj, perm):
        return (user_obj==getattr(settings,'ADMIN_LOGIN','admin'))