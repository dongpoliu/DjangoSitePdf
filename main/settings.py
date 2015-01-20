# -*- coding: UTF-8 -*-
"""
Django settings for Dongpo's Chinese picture-story book project.

"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os.path
PROJECT_ROOT   = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BASE_DIR       = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'chinese_picture_books_settings_key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'markdown_deux',
    #'django.contrib.markup',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
    'djangoratings',
    'disqus',
    'widget_tweaks',
    'guardian',
    'pdf',
    #'accounts',
    'registration',
    'profiles',    
    'main',
    'rest_framework',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',    
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
#    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.cache.CacheMiddleware',
    #'django.contrib.admindocs.middleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'main.urls'
WSGI_APPLICATION = 'main.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ATOMIC_REQUESTS': True
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
USE_I18N  = True
USE_L10N  = True
USE_TZ    = True
TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh-CN'
SITE_ID   = 1
LOCALE_PATHS  = (
    'locale',
)
LANGUAGES = (
    ('zh-CN', u'简体中文'),
    ('zh-tw', u'繁體中文'),
    ('en', u'English'),
    ('de', u'Deutsch'),
#    ('fr', u'Français'),
#    ('it', u'Italiano'),
#    ('pt', u'Português'),
#    ('es', u'Español'),
#    ('sv', u'Svenska'),
#    ('ru', u'Русский'),
#    ('jp', u'日本語'),
#    ('ko', u'한국어'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
MEDIA_URL  = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, '')
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

print  MEDIA_ROOT 
FIXTURE_DIRS  = (
    os.path.join(BASE_DIR, 'fixtures'),
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates').replace('\\','/'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.static',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += (
    "django.core.context_processors.request",
    )

AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'guardian.backends.ObjectPermissionBackend',
)

REST_FRAMEWORK = {
# Use Django's standard `django.contrib.auth` permissions,
# or allow read-only access for unauthenticated users.
        'DEFAULT_PERMISSION_CLASSES': [
               'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
               ]
        }


#Django-Guardian Settings
ANONYMOUS_USER_ID = -1
GUARDIAN_RENDER_403 = True

################## DjangoSitePdf #########################
#####################################################

# DjangoSitePdf settings for Django project
# Customize these settings only if you know

#DJANGO extended settings we are using
LOGIN_REDIRECT_URL = '/pdfdocument/'
ABSOLUTE_URL_OVERRIDES = {
        'auth.user': lambda u: "/profile/%s/" % u.username,
}
SERVER_EMAIL = "rubinliu@hotmail.com"

# apps configuration required for Django
INSTALLED_APPS += (
)

# DOMAIN will be used in link generation specially in emails
DOMAIN = '127.0.0.1:8000'

# SITE_NAME it will be used in all pages, this is the name of your website
SITE_NAME = 'Chinese Picture Books Site'

# SITE_TITLE for index pages of your website
SITE_TITLE = 'Chinese picture-book by Django'

# Meta description for SEO
SITE_DESCRIPTION = 'The Chinese picture-books site by Dongpo'

# COPYRIGHT statement for all pages
COPYRIGHT = 'Copyright &copy; 2015 Dongpo. All rights reserved.'

# SUPPORT_EMAIL address for bugs and error reporting
SUPPORT_EMAIL = 'rubinliu@hotmail.com'


################ Django-xxxxxine #####################
######################################################

