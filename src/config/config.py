from os import getenv
import os
from dotenv import load_dotenv

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

templates_path = os.path.join(project_root, 'src/templates')

load_dotenv(project_root + '/.env')

BOT_TOKEN = getenv("BOT_TOKEN")

RECONNECTION_DELAY = int(getenv("RECONNECTION_DELAY", 10))  # seconds

DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")

OPENROUTER_API_KEY = getenv("OPENROUTER_API_KEY")