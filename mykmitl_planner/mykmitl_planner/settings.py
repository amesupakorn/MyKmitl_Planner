"""
Django settings for mykmitl_planner project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
from pyexpat.errors import messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-kr2a(7rw6gsbp&)(zy44uqics*g(xev*t72my*ug%p^a-tz1jz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.humanize",
    'rest_framework',

     # แอปของ allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.mfa',
    
    'tailwind',
    'theme',
    'django_browser_reload',
    'widget_tweaks',
    
    'planner',
    'bookings',
    'chat',
    'authen',
    'channels',
]

ASGI_APPLICATION = "mykmitl_planner.asgi.application" 

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],  # ตั้งค่าให้เชื่อมต่อกับ Redis
        },
    },
}


TAILWIND_APP_NAME = 'theme'
SITE_ID = 1 

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Authentication middleware
    'allauth.account.middleware.AccountMiddleware',  # Add this line
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'chat.middleware.LoginRequiredMiddleware',
]

ROOT_URLCONF = 'mykmitl_planner.urls'

# NPM_BIN_PATH = '/usr/local/bin/npm'



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'authen', 'templates'),
            os.path.join(BASE_DIR, 'chat', 'templates'),
            os.path.join(BASE_DIR, 'bookings', 'templates'),
            os.path.join(BASE_DIR, 'planner', 'templates')
        ],
        'APP_DIRS': True,  # ให้ Django ค้นหาเทมเพลตจากโฟลเดอร์ 'templates' ของแอปใน INSTALLED_APPS
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


WSGI_APPLICATION = 'mykmitl_planner.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
       "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mykmitl", 
        "USER":  "postgres",
        "PASSWORD": "6743",
        "HOST": "localhost",
        "PORT": "8000",
    }
}

# DATABASES = {
#        "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "mykmitl", 
#         "USER":  "postgres",
#         "PASSWORD": "password",
#         "HOST": "localhost",
#         "PORT": "8000",
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Bangkok'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
            os.path.join(BASE_DIR, 'authen', 'static'),
            os.path.join(BASE_DIR, 'chat', 'static'),
            os.path.join(BASE_DIR, 'bookings', 'static'),
            os.path.join(BASE_DIR, 'planner', 'static')
]
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ตั้งค่า authentication backends สำหรับ allauth
AUTHENTICATION_BACKENDS = (
    
    'django.contrib.auth.backends.ModelBackend',  # การยืนยันตัวตนแบบปกติ
    'allauth.account.auth_backends.AuthenticationBackend',  # สำหรับ allauth
)

REST_FRAMEWORK = {
     'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',  # ใช้ session-based authentication
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # ตรวจสอบว่าผู้ใช้ต้องล็อกอิน
    ),
}

ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # บังคับให้ต้องยืนยันอีเมลก่อนล็อกอินได้
ACCOUNT_EMAIL_REQUIRED = True  # บังคับให้ผู้ใช้กรอกอีเมล

ACCOUNT_AUTHENTICATION_METHOD = "email"  # ล็อกอินด้วยอีเมลแทน username
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3  # ลิงก์ยืนยันอีเมลหมดอายุใน 3 วัน



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # เซิร์ฟเวอร์ SMTP ของผู้ให้บริการอีเมล
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'supakorn642@gmail.com'
EMAIL_HOST_PASSWORD = 'ansd zsvg xwah sngj'

# DEFAULT_FROM_EMAIL = ''  
# # ที่อยู่อีเมลที่จะใช้ในการส่ง

MEDIA_URL = '/media/'  # URL สำหรับการเข้าถึงไฟล์ที่อัปโหลด
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # ที่เก็บไฟล์ที่อัปโหลดจริง

LOGIN_URL = '/auth'