from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
import os, json

CHOOSING, TYPING_REPLY, CONFIRM = range(3)

async def broadcast(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [
            InlineKeyboardButton("Fixed", callback_data='fixed'),
            InlineKeyboardButton("Custom", callback_data='custom')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Do you want to send the fixed message or a custom message?",
                                    reply_markup=reply_markup)
    return CHOOSING

async def choosing(update: Update, context: CallbackContext) -> int:
    query=update.callback_query
    await query.answer()
    text = query.data.lower()

    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data='yes'),
            InlineKeyboardButton("No", callback_data='no')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if text == 'fixed':
        context.user_data['broadcast_message'] = "This is the fixed broadcast message."
        await query.edit_message_text(f"The message is: {context.user_data['broadcast_message']}\nPlease choose Yes or No.", reply_markup=reply_markup)
        return CONFIRM
    elif text == 'custom':
        await query.edit_message_text("Please type your custom message:")
        return TYPING_REPLY
    else:
        await query.edit_message_text("Invalid choice. Please choose 'fixed' or 'custom'.")
        return CHOOSING

async def received_message(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data='yes'),
            InlineKeyboardButton("No", callback_data='no')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data['broadcast_message'] = update.message.text
    await update.message.reply_text(f"The message is: {context.user_data['broadcast_message']}.",reply_markup=reply_markup)
    return CONFIRM

async def confirm(update: Update, context: CallbackContext) -> int:
    query=update.callback_query
    await query.answer()
    text=query.data.lower()
    if text == 'yes':
        # Read user details from user_details.json
        base_dir = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(base_dir, "..", "data", "user_details.json")

        print(f"Base directory: {base_dir}")
        print(f"File path: {file_path}")


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
        
        for detail in user_details:
            username, chat_id = detail.get("username"), detail.get("chat_id")
            message = f"Hi {username},\n\n{context.user_data['broadcast_message']}\n\nThank you!😊"
            await context.bot.send_message(chat_id=chat_id, text=message)

        message = context.user_data['broadcast_message']
        
        await query.edit_message_text(f"Broadcast message sent to all users: {message}")
        return ConversationHandler.END
    elif text == 'no':
        await query.edit_message_text("Broadcast cancelled.")
        return ConversationHandler.END
    else:
        keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data='yes'),
            InlineKeyboardButton("No", callback_data='no')
        ]
    ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Please choose.", reply_markup=reply_markup)
        return CONFIRM

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Broadcast cancelled.")
    return ConversationHandler.END
