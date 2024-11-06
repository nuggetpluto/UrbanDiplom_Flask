# config.py
import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'killeu1501')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///users.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
