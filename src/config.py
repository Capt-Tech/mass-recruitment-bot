import os
from dotenv import load_dotenv

config = {}


def read_dotenv():
    global config
    load_dotenv()
    config.update(
        {
            "TELEGRAM_BOT_API_KEY": os.getenv("TELEGRAM_BOT_API_KEY"),
            "BASE_PATH": os.getenv("BASE_PATH", "./data"),
            "WEBHOOK_SECRET": os.getenv("WEBHOOK_SECRET"),
            "WEBHOOK_URL": os.getenv("WEBHOOK_URL"),
            "PORT": os.getenv("PORT", "3000"),
            "PRODUCTION": os.getenv("PRODUCTION") == "True",
            "ADMIN_USERNAME": os.getenv("ADMIN_USERNAME", "").split(";"),
            "DEVELOPERS": os.getenv("DEVELOPERS", "").split(";"),
        }
    )
