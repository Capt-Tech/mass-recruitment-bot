from telegram import Update
from telegram.ext import CallbackContext
import constants
import file


async def registered_users(update: Update, context: CallbackContext):
    file_path = constants.get_user_details_path()
    file.ensure_directory_exists(file_path)
    user_details = file.read_user_details(file_path)

    users_registered = list(map(lambda s: "@" + s.strip().lower(), user_details.keys()))
    users_registered.sort()

    await update.effective_message.reply_text(
        f"Here are all the registered users:\n\n{'\n'.join(users_registered)}"
    )
