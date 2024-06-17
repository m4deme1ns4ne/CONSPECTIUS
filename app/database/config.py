from dotenv import load_dotenv
import os


load_dotenv()

db_config = {
    'host': 'localhost',
    'database': 'telegram_bot',
    'user': 'root',
    'password': os.getenv("MYSQLPASSWORD")
}
