import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
PGUSER = os.getenv('PGUSER')
PGPASSWORD = os.getenv('PGPASSWORD')
DATABASE = str(os.getenv('DATABASE'))
ip = os.getenv('IP')
admin_id = 454279273
chat_id = -1001942342650
