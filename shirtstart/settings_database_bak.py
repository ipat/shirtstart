# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # },
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'HOST': '192.168.59.103',
        'PORT': '49161',
        'NAME': 'xe',
        'USER': 'system',
        'PASSWORD': 'oracle',
    },
}
