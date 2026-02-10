from os import getenv
import os
from dotenv import load_dotenv

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

load_dotenv(project_root + '/.env')

TOKEN = getenv("BOT_TOKEN")