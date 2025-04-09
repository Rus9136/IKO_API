import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Используем SQLite для локального тестирования
    SQLALCHEMY_DATABASE_URI = 'sqlite:///iko_db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    ITEMS_PER_PAGE = 20