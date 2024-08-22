import re
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
    mutex_count = 0
    mutex_comms = constants.MUTEX_COMMS
    exclusive_comms_offered = []
    for comm, subcomm, pd_handle in pd_handles:
        message += f"{i}. {comm} - {subcomm} [{pd_handle}]\n"
        i += 1

        mutex_regex = mutex_comms.get(comm)
        if (
            mutex_regex
            and re.match(mutex_regex, subcomm)
            and subcomm.strip() != constants.REJECTED
        ):
            mutex_count += 1
            exclusive_comms_offered.append(f"{comm} - {subcomm}")

    if len(pd_handles) == 0:
        message += "You have not been offered any roles.\n"

    message += "\nPlease kindly accept offer(s) by sending the relevant PD(s) the following message"
    await message_fn(message)
    await message_fn(
        "I, __Name, Student No\\.__, accept the role of __role__\\.",
        parse_mode=ParseMode.MARKDOWN_V2,
    )

    j = 1
    if mutex_count > 1:
        mutex_message = (
            f"🚨 Please take note that the following offers are mutually exclusive:\n\n"
        )
        for comm in exclusive_comms_offered:
            mutex_message += f"{j}. {comm}\n"
            j += 1
        await message_fn(mutex_message)

    return ConversationHandler.END
