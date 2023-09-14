import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
PGUSER = os.getenv('PGUSER')
PGPASSWORD = os.getenv('PGPASSWORD')
DATABASE = str(os.getenv('DATABASE'))
ip = os.getenv('ip')
admin_id = [454279273, 1180411020]
chat_id = -1001699485387
    #-1001942342650