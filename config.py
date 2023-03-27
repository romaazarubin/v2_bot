import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
PGUSER = os.getenv('PGUSER')
PGPASSWORD = os.getenv('PGPASSWORD')
DATABASE = str(os.getenv('DATABASE'))
ip = os.getenv('IP')
admin_id = [5524939396, 953539403]
chat_id = -690751299