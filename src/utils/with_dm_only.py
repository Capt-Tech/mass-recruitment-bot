from telegram import Update
from telegram.ext import CallbackContext


def with_dm_only(callback):
    async def returned_callback(update: Update, context: CallbackContext):
        if update.effective_chat.type != "private":
            return await update.effective_message.reply_text(
                "This command can only be used in DMs"
            )

        return await callback(update, context)

    return returned_callback
