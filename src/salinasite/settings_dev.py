
import os

from .settings import *   #@UnusedWildImport

TEMP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'tmp'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(TEMP_DIR, 'dev.db')
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    
    'formatters': {
        'normal_format': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
    },
    
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'normal_format',
            'filename': os.path.join(TEMP_DIR, 'salina.log'),
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
    
    'loggers': {
        'django.db.backends' : {
            'handlers':['null'],
            'propagate': False,
        }
    },
    
    'root' : {
        'handlers': ['debug'],
        'level': 'DEBUG',
    }
}
    
