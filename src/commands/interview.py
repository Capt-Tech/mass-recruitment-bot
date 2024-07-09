from telegram import Update
from telegram.ext import CallbackContext


async def interview(update: Update, context: CallbackContext):
    await update.effective_message.reply_text("Hello")
