import os

class Config:
    SECRET_KEY = os.environ.get('SESSION_SECRET', 'your-secret-key-change-this')
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
