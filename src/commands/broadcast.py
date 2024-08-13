from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
from telegram.constants import ParseMode
import constants
import file
from commands.result import reply_result
import excel
import logging

logger = logging.getLogger("broadcast")

yes_no_keyboard = [
    [
        InlineKeyboardButton("Yes", callback_data=constants.YES),
        InlineKeyboardButton("No", callback_data=constants.NO),
    ]
]


async def broadcast_message(update: Update, context: CallbackContext) -> int:
    context.user_data["broadcast_type"] = constants.BroadcastType.Message

    keyboard = [
        [
            InlineKeyboardButton("Fixed", callback_data=constants.FIXED),
            InlineKeyboardButton("Custom", callback_data=constants.CUSTOM),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Do you want to send the fixed message or a custom message?",
        reply_markup=reply_markup,
    )
    return constants.ConvState.Choosing


async def broadcast_results(update: Update, context: CallbackContext) -> int:
    context.user_data["broadcast_type"] = constants.BroadcastType.Results

    reply_markup = InlineKeyboardMarkup(yes_no_keyboard)

    await update.message.reply_text(
        "Do you want to broadcast results to all users?",
        reply_markup=reply_markup,
    )
    return constants.ConvState.ConfirmBroadcast


async def choosing(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    text = query.data.lower()

    reply_markup = InlineKeyboardMarkup(yes_no_keyboard)

    if text == constants.FIXED:
        context.user_data["broadcast_message"] = "This is the fixed broadcast message."
        await query.edit_message_text(
            f"The message is:\n{context.user_data['broadcast_message']}\nPlease choose Yes or No.",
            reply_markup=reply_markup,
        )
        return constants.ConvState.ConfirmBroadcast
    elif text == constants.CUSTOM:
        await query.edit_message_text("Please type your custom message:")
        return constants.ConvState.TypingReply
    else:
        await query.edit_message_text(
            "Invalid choice. Please choose 'fixed' or 'custom'."
        )
        return constants.ConvState.Choosing


async def received_message(update: Update, context: CallbackContext) -> int:
    context.user_data["broadcast_message"] = update.message.text_html
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Skip", callback_data=constants.NO)]])
    await update.message.reply_text("Attach a photo", reply_markup=reply_markup)
    return constants.ConvState.WaitingPhoto

async def received_photo(update: Update, context: CallbackContext) -> int:
    reply_markup = InlineKeyboardMarkup(yes_no_keyboard)
    if not update.effective_message.photo or not update.effective_message.photo[0]:
        await update.callback_query.answer()
        await update.effective_message.reply_text(
          context.user_data['broadcast_message'],
          parse_mode=ParseMode.HTML,
        )
    else:
        context.user_data['broadcast_photo'] = update.effective_message.photo[0].file_id
        await update.effective_message.reply_photo(
            context.user_data['broadcast_photo'],
            context.user_data['broadcast_message'], 
            parse_mode=ParseMode.HTML,
        )
    await update.effective_message.reply_text("Confirm your message above is correct", reply_markup=reply_markup)
    return constants.ConvState.ConfirmBroadcast

async def confirm(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    text = query.data.lower()
    if text == constants.YES:
        file_path = constants.get_user_details_path()
        file.ensure_directory_exists(file_path)

        user_details = file.read_user_details(file_path)
        if not user_details:
            await query.edit_message_text(
                "User details file not found. Please ensure the file exists."
            )
            return ConversationHandler.END

        await query.edit_message_text(f"Broadcasting message...")

        failed_users = set()
        if context.user_data["broadcast_type"] == constants.BroadcastType.Message:
            for username, details in user_details.items():
                chat_id = details["chat_id"]
                try:
                    if "broadcast_photo" in context.user_data:
                        await context.bot.send_photo(chat_id, context.user_data["broadcast_photo"], caption=context.user_data['broadcast_message'], parse_mode=ParseMode.HTML)
                    else:
                        await context.bot.send_message(chat_id, context.user_data['broadcast_message'], parse_mode=ParseMode.HTML)
                except Exception as e:
                    logger.warn(f"Failed to send message to {username}: {e}")
                    failed_users.add(username)

            if len(failed_users) > 0:
                await query.edit_message_text(
                    f"Broadcast message sent to all users\n\nFailed to send to:\n{'\n'.join(map(lambda x:"@"+x,failed_users))}",
                    parse_mode=ParseMode.HTML
                )
            else:
                await query.edit_message_text(
                    "Broadcast message sent to all users",
                    parse_mode=ParseMode.HTML
                )
        elif context.user_data["broadcast_type"] == constants.BroadcastType.Results:
            sent_users = set()
            result_usernames = excel.get_result_usernames()

            for username in result_usernames:
                if username not in user_details:
                    failed_users.add(username)
                    continue
                
                chat_id = user_details[username.lower().strip()]["chat_id"]
                try:
                    await reply_result(
                        context=context, chat_id=chat_id, username=username
                    )
                    sent_users.add(username)
                except Exception as e:
                    logger.warn(f"Failed to send results to {username}: {e}")
                    failed_users.add(username)
  
            if len(failed_users) > 0:
                await query.edit_message_text(
                    f"Results broadcasted to all users\n\nFailed to send to:\n{'\n'.join(map(lambda x:"@"+x,failed_users))}",
                    parse_mode=ParseMode.HTML
                )
            else:
                await query.edit_message_text(f"Results broadcasted to all users")
        else:
            await query.edit_message_text(
                f"Invalid broadcast type: {context.user_data['broadcast_message']}"
            )
        return ConversationHandler.END
    elif text == constants.NO:
        await query.edit_message_text("Broadcast cancelled.")
        return ConversationHandler.END
