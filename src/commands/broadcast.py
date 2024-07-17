from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
import os 

CHOOSING, TYPING_REPLY, CONFIRM = range(3)

async def broadcast(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Do you want to send the fixed message or a custom message? (type 'fixed' or 'custom')")
    return CHOOSING

async def choosing(update: Update, context: CallbackContext) -> int:
    text = update.message.text.lower()
    if text == 'fixed':
        context.user_data['broadcast_message'] = "This is the fixed broadcast message."
        await update.message.reply_text(f"The message is: {context.user_data['broadcast_message']}\nType 'yes' to confirm or 'no' to cancel.")
        return CONFIRM
    elif text == 'custom':
        await update.message.reply_text("Please type your custom message:")
        return TYPING_REPLY
    else:
        await update.message.reply_text("Invalid choice. Please type 'fixed' or 'custom'.")
        return CHOOSING

async def received_message(update: Update, context: CallbackContext) -> int:
    context.user_data['broadcast_message'] = update.message.text
    await update.message.reply_text(f"The message is: {context.user_data['broadcast_message']}\nType 'yes' to confirm or 'no' to cancel.")
    return CONFIRM

async def confirm(update: Update, context: CallbackContext) -> int:
    text = update.message.text.lower()
    if text == 'yes':
        message = context.user_data['broadcast_message']
        
        # Read user details from user_details.txt
        base_dir = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(base_dir, "..", "data", "user_details.txt")

        print(f"Base directory: {base_dir}")
        print(f"File path: {file_path}")


        if not os.path.exists(file_path):
            await update.message.reply_text("User details file not found. Please ensure the file exists.")
            return ConversationHandler.END
        
        with open(file_path, "r") as file:
            lines = file.readlines()
        
        for line in lines:
            username, chat_id = line.strip().split(',')
            await context.bot.send_message(chat_id=chat_id, text=message)
        
        await update.message.reply_text(f"Broadcast message sent to all users: {message}")
        return ConversationHandler.END
    elif text == 'no':
        await update.message.reply_text("Broadcast cancelled.")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Please type 'yes' to confirm or 'no' to cancel.")
        return CONFIRM

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Broadcast cancelled.")
    return ConversationHandler.END
