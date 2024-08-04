from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
import constants
import file
from commands.result import reply_result
import excel

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
            f"The message is: {context.user_data['broadcast_message']}\nPlease choose Yes or No.",
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
    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data=constants.YES),
            InlineKeyboardButton("No", callback_data=constants.NO),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data["broadcast_message"] = update.message.text
    await update.message.reply_text(
        f"The message is: {context.user_data['broadcast_message']}.",
        reply_markup=reply_markup,
    )
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
                message = f"Hi {username},\n\n{context.user_data['broadcast_message']}\n\nThank you! 😊"
                try:
                    await context.bot.send_message(chat_id, message)
                except Exception as e:
                    print(e)
                    failed_users.add(username)

            if len(failed_users) > 0:
                await query.edit_message_text(
                    f"Broadcast message sent to all users: {context.user_data['broadcast_message']}\n\nFailed to send to:\n{'\n'.join(map(lambda x:"@"+x,failed_users))}"
                )
            else:
                await query.edit_message_text(
                    f"Broadcast message sent to all users: {context.user_data['broadcast_message']}"
                )
        elif context.user_data["broadcast_type"] == constants.BroadcastType.Results:
            sent_users = set()
            result_usernames = excel.get_result_usernames()

            for username, details in user_details.items():
                chat_id = details["chat_id"]
                try:
                    await reply_result(
                        context=context, chat_id=chat_id, username=username
                    )
                    sent_users.add(username)
                except Exception as e:
                    print(e)
                    failed_users.add(username)

            for username in result_usernames:
                if username not in sent_users:
                    failed_users.add(username)

            if len(failed_users) > 0:
                await query.edit_message_text(
                    f"Results broadcasted to all users\n\nFailed to send to:\n{'\n'.join(map(lambda x:"@"+x,failed_users))}"
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


async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Broadcast cancelled.")
    return ConversationHandler.END
