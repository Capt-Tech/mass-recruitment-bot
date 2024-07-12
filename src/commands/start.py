import constants
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler


async def start(update: Update, context: CallbackContext):
    message = constants.get_start_message(context.user_data.get("is_admin"))

    await update.effective_message.reply_text(message)
    return ConversationHandler.END
