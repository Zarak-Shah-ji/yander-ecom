import os
from decouple import config

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#SECRET_KEY = '-05sgp9!deq=q1nltm@^^2cc+v29i(tyybv3v2t77qi66czazj'
ALLOWED_HOSTS = ['127.0.0.1']
SECRET_KEY = config('SECRET_KEY')

INSTALLED_APPS = [
    'crispy_forms',
    'django_countries',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'core',
    'debug_toolbar'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'djecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


#Static files(CSS,Js,Images)

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_files')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

if ENVIRONMENT == 'production':
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#auth
AUTHENTICATION_BACKENDS = (
 # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

 # `allauth` needs this from django
    'allauth.account.auth_backends.AuthenticationBackend'
)
SITE_ID = 1
#it redirects profile pg which is needed after sign in to our homepg
LOGIN_REDIRECT_URL ='/'

#CRISPY FORMS

CRISPY_TEMPLATE_PACK = 'bootstrap4'

#Stripe Settings

#if DEBUG:
    #test keys
  #  STRIPE_PUBLISHABLE_KEY = 'pk_test_51HCND6DvfKocuQ5TITYZBNS0ie81ZauTA3kbq2tJ9PVynNyhgD0heP91NFfqlFcZqabmRIxK0pmcevrtJ0yBsPfK00gtOf4BPC'
   # STRIPE_SECRET_KEY = 'sk_test_51HCND6DvfKocuQ5TJjkQabT2yyc4PoY7lzFdSENHqHYHn12Bc00vwy8JAUdORBBLqCPuLclKixBBKLVerIQBWkkg00ZsfFvjIx'
#else:
    #LIVE KEYS
     #STRIPE_PUBLISHABLE_KEY ='pk_live_51HCND6DvfKocuQ5TS7Q8c9YmGlpjsboyxw91LKRxcK7dyIGVVMT54aCZbHeqzrzaDzqYoESyhRNnJLxWa2qmYGJF00lbJwyIob'
    #STRIPE_SECRET_KEY='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'

 
 ###for signup prob###

ACCOUNT_FORMS = {'signup': 'core.forms.MyCustomSignupForm'}



# DEBUG TOOLBAR SETTINGS

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]


def show_toolbar(request):
    return True





AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}
]

#EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')



##########################################signup prob solution#####################################################3
#This logs any emails sent to the console
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = 'yander.helpdesk@gmail.com'
EMAIL_HOST_PASSWORD = 'yander@ecom'
EMAIL_USE_TLS =True

####################################################################################################################