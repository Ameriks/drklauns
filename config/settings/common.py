import environ

ROOT_DIR = environ.Path(__file__) - 3  # (drklauns/config/settings/common.py - 3 = drklauns/)
APPS_DIR = ROOT_DIR.path('drklauns')

env = environ.Env()

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'drklauns.users.apps.UsersConfig',
    'drklauns.core.apps.CoreConfig',
    'drklauns.timetable.apps.TimetableConfig',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

DEBUG = env.bool('DJANGO_DEBUG', False)

EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

MAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = env('DJANGO_EMAIL_PASSWORD', default='')
EMAIL_HOST_USER = env('DJANGO_EMAIL_USERNAME', default='')
EMAIL_PORT = 587

ADMINS = (
    ("""Agris Ameriks""", 'd@pd.lv'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres://drklauns:drklauns@db/drklauns'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

TIME_ZONE = 'Europe/Riga'
LANGUAGE_CODE = 'lv'

SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATIC_ROOT = str(ROOT_DIR('staticfiles'))
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
)

MEDIA_ROOT = str(APPS_DIR('media'))
MEDIA_URL = '/media/'


ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_USER_MODEL = 'users.User'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}
