import excel
import constants
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from telegram.constants import ParseMode


async def verify(update: Update, context: CallbackContext):
    links = excel.get_interview_data("@" + update.effective_user.username)
    if len(links) == 0:
        await update.effective_message.reply_text(
            constants.get_username_not_found_error_msg()
        )
        return ConversationHandler.END
    message = "Please verify that you have applied for the following roles. Please contact admins regarding any issues.\n\n"
    i = 1
    for subcomm,link in links:
        message += f'{i}. {subcomm}\n'
        i += 1

    await update.effective_message.reply_text(message, parse_mode=ParseMode.HTML)
