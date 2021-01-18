import os

DEBUG = True
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, 'data/images')
DATABASE = os.path.join(BASE_DIR, 'data/mojee.db')
SCHEMA = os.path.join(BASE_DIR, 'data/schema.sql')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
