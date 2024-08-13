from config import config

import file
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
import logging


def with_command_log(command, callback):
    async def returned_callback(update: Update, context: CallbackContext):
        logger = logging.getLogger(command)
        logger.info(f"User {update.effective_user.username} used command /{command}")
        return await callback(update, context)

    return returned_callback


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


def store_user_data(callback):
    async def returned_callback(update: Update, context: CallbackContext):
        username = update.effective_user.username
        chat_id = update.message.chat_id
        file.record_user_details(username, chat_id)
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
