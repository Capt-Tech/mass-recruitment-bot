from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
import subprocess
from telegram.constants import ParseMode


async def display_logs(update: Update, context: CallbackContext) -> int:
    logs = subprocess.run(
        "docker compose logs bot", shell=True, capture_output=True
    ).stdout.decode()
    if not logs:
        logs = "No logs available"
    await update.message.reply_text(
        "```\n" + logs + "\n```",
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    return ConversationHandler.END
