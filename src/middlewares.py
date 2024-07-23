from config import config

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler


def with_dm_only(callback):
    async def returned_callback(update: Update, context: CallbackContext):
        if update.effective_chat.type != "private":
            await update.effective_message.reply_text(
                "This command can only be used in DMs"
            )
            return ConversationHandler.END

        return await callback(update, context)

    return returned_callback


def with_admin_context(callback):
    async def returned_callback(update: Update, context: CallbackContext):
        admins = config.get("ADMIN_USERNAME") + config.get("DEVELOPERS")
        if update.effective_user.username in admins:
            context.user_data["is_admin"] = True
        else:
            context.user_data["is_admin"] = False

        return await callback(update, context)

    return returned_callback


def with_admin_only(callback):
    async def returned_callback(update: Update, context: CallbackContext):
        admins = config.get("ADMIN_USERNAME") + config.get("DEVELOPERS")
        if update.effective_user.username not in admins:
            await update.effective_message.reply_text(
                "This command can only be used by admins"
            )
            return ConversationHandler.END
        return await callback(update, context)

    return returned_callback

