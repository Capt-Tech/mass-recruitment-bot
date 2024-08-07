import excel
import constants
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from telegram.constants import ParseMode


async def result(update: Update, context: CallbackContext):
    await reply_result(update=update, context=context)


async def reply_result(
    update: Update = None,
    context: CallbackContext = None,
    chat_id: int = None,
    username: str = None,
):
    if username == None:
        username = update.effective_user.username
        message_fn = update.effective_message.reply_text
    else:

        async def message_fn(msg, parse_mode=None):
            await context.bot.send_message(chat_id, msg, parse_mode=parse_mode)

    pd_handles = excel.get_result_data("@" + username)
    if pd_handles == None:
        await message_fn(constants.get_username_not_found_error_msg())
        return ConversationHandler.END
    if len(pd_handles) == 0:
        await message_fn("You have not been offered any roles.")
        return ConversationHandler.END

    message = "Hi, these are the statuses of roles you applied for:\n\n"
    i = 1
    for comm, subcomm, pd_handle in pd_handles:
        message += f"{i}. {comm} - {subcomm} [{pd_handle}]\n"
        i += 1
    message += "\nPlease kindly accept one offer by sending the relevant PD the following message"
    await message_fn(message)
    await message_fn(
        "I, __Name, Student No\\.__, accept the role of __role__\\.",
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    return ConversationHandler.END
