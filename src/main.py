import logging
import asyncio
import commands
import callbacks
import constants
import middlewares
from telegram import Bot
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)
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


async def set_commands():
    await TBOT.set_my_commands(constants.COMMANDS.items())


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_commands())

    application = (
        Application.builder().token(config.get("TELEGRAM_BOT_API_KEY")).build()
    )

    application.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler(
                    "start",
                    middlewares.with_command_log(
                        "start",
                        middlewares.with_admin_context(
                            middlewares.with_dm_only(commands.start)
                        ),
                    ),
                ),
                CommandHandler(
                    "verify",
                    middlewares.with_command_log(
                        "verify",
                        middlewares.with_dm_only(
                            middlewares.store_user_data(commands.verify)
                        ),
                    ),
                ),
                CommandHandler(
                    "result",
                    middlewares.with_command_log(
                        "result",
                        middlewares.with_dm_only(
                            middlewares.store_user_data(commands.result)
                        ),
                    ),
                ),
                CommandHandler(
                    "upload_verify",
                    middlewares.with_dm_only(
                        middlewares.with_admin_only(
                            middlewares.store_user_data(commands.upload_verify)
                        )
                    ),
                ),
                CommandHandler(
                    "upload_result",
                    middlewares.with_dm_only(
                        middlewares.with_admin_only(
                            middlewares.store_user_data(commands.upload_result)
                        )
                    ),
                ),
                CommandHandler(
                    "broadcast_message",
                    middlewares.with_dm_only(
                        middlewares.with_admin_only(
                            middlewares.store_user_data(commands.broadcast_message)
                        )
                    ),
                ),
                CommandHandler(
                    "broadcast_results",
                    middlewares.with_dm_only(
                        middlewares.with_admin_only(
                            middlewares.store_user_data(commands.broadcast_results)
                        )
                    ),
                ),
            ],
            states={
                constants.ConvState.RequestVerifyExcel: [
                    MessageHandler(
                        filters.Document.FileExtension("csv"),
                        callbacks.receive_upload_excel,
                    )
                ],
                constants.ConvState.RequestResultExcel: [
                    MessageHandler(
                        filters.Document.FileExtension("csv"),
                        callbacks.receive_upload_excel,
                    )
                ],
                constants.ConvState.Choosing: [
                    CallbackQueryHandler(commands.choosing, pattern="^fixed|custom$")
                ],
                constants.ConvState.TypingReply: [
                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND, commands.received_message
                    )
                ],
                constants.ConvState.ConfirmBroadcast: [
                    CallbackQueryHandler(commands.confirm, pattern="^yes|no$")
                ],
                constants.ConvState.WaitingPhoto: [
                    CallbackQueryHandler(commands.received_photo),
                    MessageHandler(
                        filters.PHOTO & ~filters.COMMAND, commands.received_photo
                    ),
                ],
            },
            fallbacks=[
                CommandHandler(
                    "start",
                    middlewares.with_admin_context(
                        middlewares.with_dm_only(commands.start)
                    ),
                ),
                CommandHandler("cancel", commands.cancel),
            ],
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
            secret_token=config.get("WEBHOOK_SECRET"),
            port=config.get("PORT"),
            webhook_url=config.get("WEBHOOK_URL"),
        )
    else:
        application.run_polling()


if __name__ == "__main__":
    main()
