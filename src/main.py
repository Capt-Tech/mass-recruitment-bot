import logging
import commands
from telegram import Bot
from telegram.ext import Application, CommandHandler
from config import config, read_dotenv

read_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("apscheduler.scheduler").setLevel(logging.WARNING)
logging.getLogger("apscheduler.executors.default").setLevel(logging.WARNING)

logger = logging.getLogger("main")

TBOT = Bot(config.get("TELEGRAM_BOT_API_KEY"))

COMMANDS_DICT = {
    "start": "Display help page",
    "interview": "Book an interview slot",
    "result": "Get outcome",
}

TBOT.set_my_commands(COMMANDS_DICT.items())


def main():
    application = (
        Application.builder().token(config.get("TELEGRAM_BOT_API_KEY")).build()
    )

    application.add_handler(CommandHandler("start", commands.start))
    application.add_handler(CommandHandler("interview", commands.interview))
    application.add_handler(CommandHandler("result", commands.result))

    application.add_error_handler(
        lambda update, context: logger.error(
            f"Update {update} caused error: {context.error}"
        )
    )

    if config.get("PRODUCTION"):
        logger.info("Running on webhook")
        application.run_webhook(
            listen="0.0.0.0",
            port=config.get("PORT"),
            webhook_url=config.get("WEBHOOK_URL"),
        )
    else:
        application.run_polling()


if __name__ == "__main__":
    main()
