import os
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {0} environment variable.".format(var_name)
        raise ImproperlyConfigured(error_msg)

SITE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ps1auth',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, "static")

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    #'django.template.loaders.cached.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    # Begin Non Default Template Context processors
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'ps1auth.urls'

# Python dotted patH to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ps1auth.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #os.path.join(SITE_ROOT, "templates"),
)

PROJECT_APPS = (
    'ps1auth',
    'accounts',
    'rfid',
    'zoho_integration',
    'memberpoint',
#    'paypal_integration',
    'member_management',
    'crm',
    'signup',
)

INSTALLED_APPS = (
    'bootstrap3',
    'bootstrap3_datetime',
    'django.contrib.webdesign',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'djcelery',
    'reversion',
    'django_tables2',
    #'paypal.standard.ipn',
    #'billing',
)

POST_INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
)

INSTALLED_APPS = INSTALLED_APPS + PROJECT_APPS + POST_INSTALLED_APPS


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar_full':[
            ["Source","Save","NewPage","DocProps","Preview","Print","Templates","document"],
            ["Cut","Copy","Paste","PasteText","PasteFromWord","Undo","Redo"],
            ["Find","Replace","SelectAll","Scayt"],
            ["Form","Checkbox","Radio","TextField","Textarea","Select","Button","ImageButton","HiddenField"],
            ["Bold","Italic","Underline","Strike","Subscript","Superscript","RemoveFormat"],
            ["NumberedList","BulletedList","Outdent","Indent","Blockquote","CreateDiv","JustifyLeft","JustifyCenter","JustifyRight","JustifyBlock","BidiLtr","BidiRtl"],
            ["Link","Unlink","Anchor"],
            ["CreatePlaceholder","Image","Flash","Table","HorizontalRule","Smiley","SpecialChar","PageBreak","Iframe","InsertPre"],
            ["Styles","Format","Font","FontSize"],
            ["TextColor","BGColor"],
            ["UIColor","Maximize","ShowBlocks"],
            ["button1","button2","button3","oembed","MediaEmbed"],
            ["About"],
        ],
        'toolbar_standard':[
            ["Cut","Copy","Paste","PasteText","PasteFromWord",'-',"Undo","Redo"],
            ["Scayt"],
            ["Link","Unlink","Anchor"],
            ["Image","Table","HorizontalRule","SpecialChar"],
            ["Maximize"],
            ["Source"],
            ["Bold","Italic","Underline","-","RemoveFormat"],
            ["NumberedList","BulletedList","-","Outdent","Indent","-","Blockquote"],
            ["Styles","Format"],
            ["About"],
        ],
        'width': 704,
        'toolbar': 'standard',
    }
}

AUTHENTICATION_BACKENDS = (
    'accounts.backends.PS1Backend',
)

AUTH_USER_MODEL = 'accounts.PS1User'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
LOGIN_REDIRECT_URL = '/zinc/member_list'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'


SECRET_KEY = get_env_variable('SECRET_KEY')
AD_URL = get_env_variable('AD_URL')
AD_DOMAIN = get_env_variable('AD_DOMAIN')
AD_BASEDN = get_env_variable('AD_BASEDN')
AD_BINDDN = get_env_variable('AD_BINDDN')
AD_BINDDN_PASSWORD = get_env_variable('AD_BINDDN_PASSWORD')
ZOHO_AUTHTOKEN = get_env_variable('ZOHO_AUTHTOKEN')

TEST_RUNNER = 'django.test.runner.DiscoverRunner'
