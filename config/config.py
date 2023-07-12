# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    APP_ROOT = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_ROOT, os.pardir))
    SECRET_KEY = os.getenv("SECRET_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = False
    PAGE_SIZE = os.getenv("PAGE_SIZE", 50)
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_RECORD_QUERIES = True


class TestConfig(Config):
    ENV = "test"
    DEBUG = True
    TESTING = True
