from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
import os, json
import constants

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
        if not os.path.exists(file_path):
            await update.message.reply_text("User details file not found. Please ensure the file exists.")
            return ConversationHandler.END
        else:
            try:
                with open(file_path, "r") as file:
                    content = file.read().strip()
                    if content:
                        user_details = json.loads(content)
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Error reading JSON file: {e}. Initializing with an empty list.")
        
        for username, details in user_details.items():
            chat_id = details["chat_id"]
            message = f"Hi {username},\n\n{context.user_data['broadcast_message']}\n\nThank you!😊"
            await context.bot.send_message(chat_id=chat_id, text=message)

        message = context.user_data['broadcast_message']
        
        await query.edit_message_text(f"Broadcast message sent to all users: {message}")
        return ConversationHandler.END
    elif text == constants.NO:
        await query.edit_message_text("Broadcast cancelled.")
        return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Broadcast cancelled.")
    return ConversationHandler.END
