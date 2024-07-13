import excel
import constants
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler


async def result(update: Update, context: CallbackContext):
    pd_handles = excel.get_result_data("@" + update.effective_user.username)
    if len(pd_handles) == 0:
        await update.effective_message.reply_text(
            constants.get_username_not_found_error_msg()
        )
        return ConversationHandler.END
    message = "Hi, you have been offered the following roles:\n\n"
    i = 1
    for subcomm, pd_handle in pd_handles:
        message += f"{i}. {subcomm} - {pd_handle}\n"
        i += 1
    message += "\nPlease kindly accept one offer by sending the relevant PD the following message"
    await update.effective_message.reply_text(message)
    await update.effective_message.reply_text(
        "I, __Name, Student No\\.__, accept the role of __role__\\.",
        parse_mode="MarkdownV2",
    )
