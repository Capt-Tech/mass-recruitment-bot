import excel
import constants
import middlewares
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler


async def interview(update: Update, context: CallbackContext):
    links = excel.get_interview_data("@" + update.effective_user.username)
    if len(links) == 0:
        await update.effective_message.reply_text(
            constants.get_username_not_found_error_msg()
        )
        return ConversationHandler.END
    message = "You have applied for the following roles. Please sign up for an interview slot with the link provided.\n\n"
    i = 1
    for subcomm, link in links:
        message += f'{i}. {subcomm} - <a href="{link}">Book Interview</a>\n'
        i += 1
    
    username = update.effective_user.username
    chat_id = update.message.chat_id
    middlewares.record_user_details(username, chat_id)

    await update.effective_message.reply_text(message, parse_mode="HTML")
