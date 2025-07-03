import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    JWT_SECRET_KEY = 'your-secret-key'

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}