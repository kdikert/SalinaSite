
import sys


DEBUG = True

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = '6@txscd*u@r$)pd47%5yux^%-mxcguq9#bvban=!zc3u8&amp;*u5d'

SITE_ID = 1

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Amsterdam'

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# Restrict languages to those that BedSense applications have translations
ugettext = lambda s: s # This is some trick to avoid circular import in i18n machinery
LANGUAGES = (
    ('en', ugettext('English')),
    ('nl', ugettext('Dutch')),
)

# Absolute directory path to the directory that holds uploaded media. This
# setting is used only when saving uploaded content. The Django application
# must have write permissions to this location, as it will write the files
# here. In the production environment this directory must be set up to be
# served through the web server. In the development environment there are
# URLs set up which can serve the files in this directory.
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Note that these files are
# the ones that have been uploaded to the service, not the regular static media.
# Make sure to use a trailing slash if there is a path component (optional in
# other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
# ---
# A separate web server must be set up to serve this path. If this is a
# relative URL (no schema and host part) the media is obviously hosted on
# the same server. 
MEDIA_URL = ''

# Absolute directory path to the directory that holds static files for the site.
# This is used by the manage.py collectstatic command to know where to copy
# the static files.
STATIC_ROOT = ''

# A URL prefix that identifies that the resource in question is a static file.
# This URL prefix must be separately set up to serve files from the STATIC_ROOT
# directory.
# ---
# A separate web server must be set up to serve this path. If this is a
# relative URL (no schema and host part) the media is obviously hosted on
# the same server. 
STATIC_URL = '/static/'

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.FileSystemFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
#    'django.template.loaders.filesystem.Loader',
#    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'salinasite.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'salinasite.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
#    'south',
    'salina',
    
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    
    'formatters': {
        'normal_format': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
    },
    
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'normal_format',
            'filename': '/home/salina/salina.log',
            'mode': 'a',
            'maxBytes': (2 ** 25),
            'backupCount': 1,
        },
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'normal_format',
            'stream': sys.stdout,
        },
    },
    
#    'loggers': {},
    
    'root' : {
        'handlers': ['file'],
        'level': 'DEBUG',
    }
}

# Custom settings

TEMP_DIR = '/home/salina/tmp'

