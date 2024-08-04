from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
import os, json
import constants
import file

async def broadcast(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [
            InlineKeyboardButton("Fixed", callback_data = constants.FIXED),
            InlineKeyboardButton("Custom", callback_data = constants.CUSTOM)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Do you want to send the fixed message or a custom message?",
                                    reply_markup=reply_markup)
    return constants.ConvState.Choosing

async def choosing(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    text = query.data.lower()

    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data = constants.YES),
            InlineKeyboardButton("No", callback_data = constants.NO)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if text == constants.FIXED:
        context.user_data['broadcast_message'] = "This is the fixed broadcast message."
        await query.edit_message_text(f"The message is: {context.user_data['broadcast_message']}\nPlease choose Yes or No.", reply_markup=reply_markup)
        return constants.ConvState.Confirm
    elif text == constants.CUSTOM:
        await query.edit_message_text("Please type your custom message:")
        return constants.ConvState.TypingReply
    else:
        await query.edit_message_text("Invalid choice. Please choose 'fixed' or 'custom'.")
        return constants.ConvState.Choosing

async def received_message(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data = constants.YES),
            InlineKeyboardButton("No", callback_data = constants.NO)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['broadcast_message'] = update.message.text
    await update.message.reply_text(f"The message is: {context.user_data['broadcast_message']}.", reply_markup=reply_markup)
    return constants.ConvState.Confirm

async def confirm(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    text = query.data.lower()
    if text == constants.YES:
        file_path = constants.get_user_details_path()
        file.ensure_directory_exists(file_path)

        user_details = file.read_user_details(file_path)
        if not user_details:
            await query.edit_message_text("User details file not found. Please ensure the file exists.")
            return ConversationHandler.END

        for username, details in user_details.items():
            chat_id = details["chat_id"]
            message = f"Hi {username},\n\n{context.user_data['broadcast_message']}\n\nThank you!😊"
            await context.bot.send_message(chat_id=chat_id, text=message)

        await query.edit_message_text(f"Broadcast message sent to all users: {context.user_data['broadcast_message']}")
        return ConversationHandler.END
    elif text == constants.NO:
        await query.edit_message_text("Broadcast cancelled.")
        return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Broadcast cancelled.")
    return ConversationHandler.END
