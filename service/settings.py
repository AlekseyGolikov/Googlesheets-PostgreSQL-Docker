# settings.py

import os

DATABASE = {
    'HOST': os.environ['DB_HOST'],
    'PORT': os.environ['DB_PORT'],
    'NAME': os.environ['DB_NAME'],
    'USER': os.environ['DB_USER'],
    'PASSWORD': os.environ['DB_PASSWORD'],
}

TG_BOT = {
    'TG_CHAT': os.environ['TG_CHAT'],
    'TG_TOKEN': os.environ['TG_TOKEN']
}

