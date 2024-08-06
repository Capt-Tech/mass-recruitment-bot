from telegram import Update
from telegram.ext import CallbackContext
import constants


async def upload_verify(update: Update, context: CallbackContext) -> int:
    await update.effective_message.reply_text(
        "Please upload the verification excel file in csv format."
    )
    context.user_data["state"] = constants.ConvState.RequestVerifyExcel
    return constants.ConvState.RequestVerifyExcel
