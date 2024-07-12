from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
import constants
import excel


async def receive_upload_excel(update: Update, context: CallbackContext) -> int:
    path = None
    state = context.user_data["state"]
    if state == constants.ConvState.RequestInterviewExcel:
        path = constants.get_interview_path()
    else:
        raise Exception(f"Invalid interview file upload state: {state}")

    await update.effective_message.reply_text(
        "File received. Please wait while I process it..."
    )
    file = await update.message.document.get_file()
    await file.download_to_drive(path)
    print(f"File saved to {path}")
    if not excel.validate_interview_file(path):
        await update.effective_message.reply_text(
            "Unable to parse file. Please try again."
        )
        return constants.ConvState.RequestInterviewExcel

    await update.effective_message.reply_text("File processed successfully.")
    return ConversationHandler.END
