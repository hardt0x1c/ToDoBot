import os
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_NAME = os.getenv('BOT_NAME')
ADMIN_ID = os.getenv('ADMIN_ID')
ADMIN_NAME = os.getenv('ADMIN_NAME')
