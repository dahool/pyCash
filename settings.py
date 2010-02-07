# Django settings for pyCash project.
import os
import logging

PROJECT_PATH = os.path.normpath(os.path.abspath(os.path.dirname(__file__)))

isProd = os.path.exists(os.path.join(PROJECT_PATH,"prod.key"))

VERSION = "0.8.2"
APPLICATION = "pyCash"

JQUERY_VERSION = '1.3.2'
EXT_VERSION = '2.2.1'

DEV = not isProd
#DEBUG = DEV
DEBUG = True
TEMPLATE_DEBUG = DEBUG
LOG_LEVEL = logging.DEBUG
 
ADMINS = (
    ('Admin','admin@localhost'),
)

MANAGERS = ADMINS

if isProd:
    DATABASE_ENGINE = 'mysql'
    DATABASE_NAME = 'expenses'
    DATABASE_USER = 'root'
    DATABASE_PASSWORD = 'root'
    DATABASE_HOST = ''
    DATABASE_PORT = ''
else:    
    DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    DATABASE_NAME = 'exp'             # Or path to database file if using sqlite3.
    DATABASE_USER = 'root'             # Not used with sqlite3.
    DATABASE_PASSWORD = 'root'         # Not used with sqlite3.
    DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Argentina/Buenos_Aires'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = '5894g(v(td&*gb^0vd11r&#2$1i^2^yz#-zka^)@&tq^))_p0c'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'pyCash.urls'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

MEDIA_ROOT = os.path.join(PROJECT_PATH,'pages','media')

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH,'pages'),
)

if isProd:
    MEDIA_URL = 'http://py.banshee.sgt/media/'    
    GOOGLE_USER = "cash.tax.service@gmail.com"
    GOOGLE_PASS = "0vd11taxservice" 
    
    LOG_FILE = '/tmp/pycash-debug.log'
else:
    if os.name == "posix":
        pass
    else:
        os.environ['https_proxy']
        os.environ['http_proxy']
        #os.environ['proxy_username']
        #os.environ['proxy_password'] 

    LOG_FILE = '/tmp/pycash-debug-dev.log'
    MEDIA_ROOT = os.path.join(PROJECT_PATH,'pages','media')
    MEDIA_URL = 'http://localhost:8000/cash/media/'
    GOOGLE_USER = "verbum-noreply@os-translation.com.ar"
    GOOGLE_PASS = "coyote16"

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

AUTHENTICATION_BACKENDS = ('pyCash.settings_auth.SettingsAuthBackend',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'pyCash.cash',
    #'django_evolution',
)
