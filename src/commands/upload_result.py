from telegram import Update
from telegram.ext import CallbackContext
import constants


async def upload_result(update: Update, context: CallbackContext) -> int:
    await update.effective_message.reply_text(
        "Please upload the result and outcomes excel file in csv format."
    )
    context.user_data["state"] = constants.ConvState.RequestResultExcel
    return constants.ConvState.RequestResultExcel
