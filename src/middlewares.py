from config import config
import os
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

def record_user_details(username, chat_id):
    # getting the path to user_details.txt which is in the directory as middlewares.py
    base_dir = os.path.dirname(os.path.dirname(__file__)) 
    file_path = os.path.join(base_dir, "data", "user_details.txt")  

    with open(file_path, "r+") as file:
        lines = file.readlines()
        for line in lines:
            if f"{username},{chat_id}\n" in line:
                return 

        # If not found in txt , write the user details at the end of the file
        file.write(f"{username},{chat_id}\n")
        print("Details recorded")
