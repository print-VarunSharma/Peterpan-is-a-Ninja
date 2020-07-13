import django_heroku
import os
import sys
from django.conf import settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+wb%6mjgq%owt5gop2=+_dk6b9n3qpn2@s2%6^it36^*-(7^34'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 5a0ee679534801eb77165788e98b9ef90a440b289d585e95

ALLOWED_HOSTS = ['ninjasiteapp.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'gallery',
    'imagekit',
    # 'whitenoise.runserver_nostatic',

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

    'crispy_forms',
    'tinymce',

    'marketing',
    'posts',
    'gunicorn',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ninjasite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'ninjasite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'ninjasite',
            'USER': 'ninja_admin',
            'PASSWORD': 'Apollo15',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_DIR = os.path.join(BASE_DIR, 'posts/media')

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_in_env')]
STATIC_ROOT = os.path.join(BASE_DIR, 'posts/staticfiles')
STATIC_URL = '/static/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# STATIC_HOST = os.environ.get('DJANGO_STATIC_HOST', '')
# STATIC_URL = STATIC_HOST + '/static/'

# Tinymce

TINYMCE_DEFAULT_CONFIG = {
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': '''
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}

MAILCHIMP_API_KEY = ''
MAILCHIMP_DATA_CENTER = ''
MAILCHIMP_EMAIL_LIST_ID = ''

# Django Allauth

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)

SITE_ID = 1

# ------------------------------Gallery --------------------------------
# Location of logo in static
GALLERY_LOGO_PATH = getattr(
    settings, 'GALLERY_LOGO_PATH', "gallery/images/starcross.png")
# Gallery title in top bar
GALLERY_TITLE = getattr(settings, 'GALLERY_TITLE', "Gallery")
# Info text in footer
GALLERY_FOOTER_INFO = getattr(
    settings, 'GALLERY_FOOTER_INFO', "Starcross Gallery")

# Target height for thumbnail display
GALLERY_THUMBNAIL_SIZE = getattr(settings, 'GALLERY_THUMBNAIL_SIZE', 250)
# Large preview in modal popup, enough to fill a typical browser window
GALLERY_PREVIEW_SIZE = getattr(settings, 'GALLERY_PREVIEW_SIZE', 1000)
# JPEG encoding quality
GALLERY_RESIZE_QUALITY = getattr(settings, 'GALLERY_RESIZE_QUALITY', 80)
# Multiple used to increase quality on high resolution screens. Default to double
GALLERY_HDPI_FACTOR = getattr(settings, 'GALLERY_HDPI_FACTOR', 2)
# Image margin as float
GALLERY_IMAGE_MARGIN = getattr(settings, 'GALLERY_IMAGE_MARGIN', 6.0)
# CSS Color Styling
GALLERY_THEME_COLOR = getattr(settings, 'GALLERY_THEME_COLOR', "black")

django_heroku.settings(locals())
