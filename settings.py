# Django settings for pyCash project.
import os
import logging

PROJECT_PATH = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))

isProd = os.path.exists(os.path.join(PROJECT_PATH,"prod.key"))

VERSION = "0.9.1"
APPLICATION = "Cash Manager"
MOBILE_VERSION = "1.1.0"

###### libraries
JQUERY_VERSION = '1.7.1'
EXT_VERSION = '2.2.1'

DEV = not isProd
DEBUG = DEV
#DEBUG = True
TEMPLATE_DEBUG = DEBUG
LOG_LEVEL = logging.DEBUG
 
ADMINS = (
    ('Admin','admin@localhost'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'NAME': os.path.join(PROJECT_PATH,"expenses.db"),
        'ENGINE': 'django.db.backends.sqlite3',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
    },
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Argentina/Buenos_Aires'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = '[[SECRET_KEY]]'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'cash.auth.middleware.RemoteTokenMiddleware',
	'cash.loginrequiredmiddleware.LoginRequiredMiddleware',
    'django_mobile.middleware.MobileMiddleware',
)

ROOT_URLCONF = 'urls'

LOGIN_URL = '/login'
LOGIN_EXEMPT_URLS = '/token'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login'
# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

MEDIA_ROOT = os.path.join(PROJECT_PATH,'media_store')
STATIC_ROOT = os.path.join(PROJECT_PATH, 'media')

MEDIA_URL = '/site_store/'
STATIC_URL = '/media/'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH,'pages'),
)

MOBILE_UTILS_SETTINGS = {
    'MOBILE_TEMPLATES_DIR': (
        os.path.join(PROJECT_PATH,'mobile'),
    ),
    'IGNORE_LIST':[],                        #tuple of browsers to ignore    
    'USER_AGENTS_FILE': os.path.join(PROJECT_PATH,'django_mobile','data','mobile_agents.txt'),  # line-broken strings to match
    'USE_REGEX':False                      # use RegEx to do the string search
}

EXT_LOCATION = 'js/ext/' + EXT_VERSION + '/'
UX_LOCATION = EXT_LOCATION + 'ux/'

if isProd:
    EXT_FILES = ['js/jquery/jquery-' + JQUERY_VERSION + '.min.js',
                 EXT_LOCATION + 'adapter/jquery/ext-jquery-adapter.js',
                 EXT_LOCATION + 'ext-all.js']
else:
    EXT_FILES = ['js/jquery/jquery-' + JQUERY_VERSION + '.min.js',
                 EXT_LOCATION + 'adapter/jquery/ext-jquery-adapter.js',
                 EXT_LOCATION + 'ext-all-debug.js']
    
USE_GOOGLE_CAL = True

#AUTHENTICATION_BACKENDS = ('pyCash.settings_auth.SettingsAuthBackend',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'cash',
)

RPC_HOST = 'http://localhost:8081/xmlrpc/'
if isProd:
    LOG_FILE = '/tmp/pycash-debug.log'
else:
    LOG_FILE = '/tmp/pycash-debug-dev.log'
    
try:
    execfile(os.path.join(PROJECT_PATH,'settings_local.py'))
except IOError:
    GOOGLE_USER = "-"
    GOOGLE_PASS = "-" 
