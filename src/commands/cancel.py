from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler


async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Operation cancelled")
    return ConversationHandler.END
