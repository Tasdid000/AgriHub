"""
Django settings for agrihub project.

Generated by 'django-admin startproject' using Django 3.2.20.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$ys8c41g8appuc9q8njerezn6t8znv60-bed)3us__e9zm34&b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    "corsheaders",
    'rest_framework',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
    'meeting',
    'rest_framework_simplejwt',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

PASSWORD_RESET_TIMEOUT = 900

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_FROM')

ZOOM_CLIENT_ID = os.getenv('ZOOM_CLIENT_ID')
ZOOM_CLIENT_SECRET = os.getenv('ZOOM_CLIENT_SECRET')
ZOOM_REDIRECT_URI = 'http://localhost:8000/zoom/callback/'

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=20),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=5),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "email",
    "USER_ID_CLAIM": "user_email",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",
    
}
CROS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'agrihub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'agrihub.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'agrihub',
        'HOST': 'localhost',
        'PASSWORD': '',
        'USER': 'root',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'home.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# ASGI_APPLICATION = 'House_Rent.asgi.application'

# customColorPalette = [
#     {"color": "hsl(4, 90%, 58%)", "label": "Red"},
#     {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
#     {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
#     {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
#     {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
#     {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
# ]

# CKEDITOR_5_CONFIGS = {
#     "default": {
#         "toolbar": [
#             "heading",
#             "|",
#             "bold",
#             "italic",
#             "link",
#             "bulletedList",
#             "numberedList",
#             "blockQuote",
#             "imageUpload"
#         ],
#     },
#     "comment": {
#         "language": {"ui": "en", "content": "en"},
#         "toolbar": [
#             "heading",
#             "|",
#             "bold",
#             "italic",
#             "link",
#             "bulletedList",
#             "numberedList",
#             "blockQuote",
#         ],
#     },
#     "extends": {
#         "language": "en",
#         "blockToolbar": [
#             "paragraph",
#             "heading1",
#             "heading2",
#             "heading3",
#             "|",
#             "bulletedList",
#             "numberedList",
#             "|",
#             "blockQuote",
#         ],
#         "toolbar": [
#             # "heading",
#             # "codeBlock",
#             # "|",
            
#             # "|",
#             "bold",
#             "italic",
#             # "link",
#             "underline",
#             "strikethrough",
#             # "code",
#             # "subscript",
#             # "superscript",
#             # "highlight",
#             "|",
#             "bulletedList",
#             # "numberedList",
#             # "todoList",
#             # "|",
#             # "outdent",
#             # "indent",
#             # "|",
#             # "blockQuote",
#             # "insertImage",
#             # "|",
#             # "fontSize",
#             # "fontFamily",
#             # "fontColor",
#             # "fontBackgroundColor",
#             # "mediaEmbed",
#             "removeFormat",
#             # "insertTable",
#             # "sourceEditing",
#         ],
#         "image": {
#             "toolbar": [
#                 "imageTextAlternative",
#                 "|",
#                 "imageStyle:alignLeft",
#                 "imageStyle:alignRight",
#                 "imageStyle:alignCenter",
#                 "imageStyle:side",
#                 "|",
#                 "toggleImageCaption",
#                 "|"
#             ],
#             "styles": [
#                 "full",
#                 "side",
#                 "alignLeft",
#                 "alignRight",
#                 "alignCenter",
#             ],
#         },
#         "table": {
#             "contentToolbar": [
#                 "tableColumn",
#                 "tableRow",
#                 "mergeTableCells",
#                 "tableProperties",
#                 "tableCellProperties",
#             ],
#             "tableProperties": {
#                 "borderColors": customColorPalette,
#                 "backgroundColors": customColorPalette,
#             },
#             "tableCellProperties": {
#                 "borderColors": customColorPalette,
#                 "backgroundColors": customColorPalette,
#             },
#         },
#         "heading": {
#             "options": [
#                 {
#                     "model": "paragraph",
#                     "title": "Paragraph",
#                     "class": "ck-heading_paragraph",
#                 },
#                 {
#                     "model": "heading1",
#                     "view": "h1",
#                     "title": "Heading 1",
#                     "class": "ck-heading_heading1",
#                 },
#                 {
#                     "model": "heading2",
#                     "view": "h2",
#                     "title": "Heading 2",
#                     "class": "ck-heading_heading2",
#                 },
#                 {
#                     "model": "heading3",
#                     "view": "h3",
#                     "title": "Heading 3",
#                     "class": "ck-heading_heading3",
#                 },
#             ]
#         },
#         "list": {
#             "properties": {
#                 "styles": True,
#                 "startIndex": True,
#                 "reversed": True,
#             }
#         },
#         "htmlSupport": {
#             "allow": [
#                 {"name": "/.*/", "attributes": True, "classes": True, "styles": True}
#             ]
#         },
#     },
# }

# CKEDITOR_UPLOAD_PATH = 'uploads/'
# JAZZMIN_SETTINGS = {
#     "site_title": "StudySolution",
#     "welcome_sign": "Hey there...welcome back",
#     "site_header": "StudySolution",
#     "site_brand": "StudySolution",
#     "copyright": "www.studysolution.com",
# }


# JAZZMIN_UI_TWEAKS = {
#     "navbar_small_text": False,
#     "footer_small_text": False,
#     "body_small_text": False,
#     "brand_small_text": False,
#     "brand_colour": "navbar-success",
#     "accent": "accent-teal",
#     "navbar": "navbar-dark",
#     "no_navbar_border": False,
#     "navbar_fixed": False,
#     "layout_boxed": False,
#     "footer_fixed": False,
#     "sidebar_fixed": False,
#     "sidebar": "sidebar-dark-info",
#     "sidebar_nav_small_text": False,
#     "sidebar_disable_expand": False,
#     "sidebar_nav_child_indent": False,
#     "sidebar_nav_compact_style": False,
#     "sidebar_nav_legacy_style": False,
#     "sidebar_nav_flat_style": False,
#     "theme": "cyborg",
#     "dark_mode_theme": None,
#     "button_classes": {
#         "primary": "btn-primary",
#         "secondary": "btn-secondary",
#         "info": "btn-info",
#         "warning": "btn-warning",
#         "danger": "btn-danger",
#         "success": "btn-success",
#     },
# }
# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
# Media Files
MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.1.4:3000",
]
CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
