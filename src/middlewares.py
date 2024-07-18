from config import config
import os, json
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
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "data", "user_details.json")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Initialize an empty list for storing user details
    user_details = []

    # Read existing data from the JSON file if it exists
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as file:
                content = file.read().strip()
                if content:
                    user_details = json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error reading JSON file: {e}. Initializing with an empty list.")

    # Check if the user details are already present
    for user in user_details:
        if user.get("username") == username and user.get("chat_id") == chat_id:
            return

    # If not found in JSON, add the new user details
    user_details.append({"username": username, "chat_id": chat_id})

    # Write the updated user details back to the JSON file
    with open(file_path, "w") as file:
        json.dump(user_details, file, indent=4)

    print("Details recorded")
