import logging
import commands
import callbacks
import constants
from telegram import Bot
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from config import config, read_dotenv
from utils import with_dm_only

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

    application.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler("start", with_dm_only(commands.start)),
                CommandHandler("interview", with_dm_only(commands.interview)),
                CommandHandler("result", with_dm_only(commands.result)),
                CommandHandler(
                    "upload_interview", with_dm_only(commands.upload_interview)
                ),
            ],
            states={
                constants.ConvState.RequestInterviewExcel: [
                    MessageHandler(
                        filters.Document.FileExtension("csv"),
                        callbacks.receive_upload_excel,
                    )
                ]
            },
            fallbacks=[CommandHandler("start", with_dm_only(commands.start))],
        )
    )

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
