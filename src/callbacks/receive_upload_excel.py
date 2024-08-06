from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
import constants
import excel
import shutil


async def receive_upload_excel(update: Update, context: CallbackContext) -> int:
    path = None
    tmp_path = None
    state = context.user_data["state"]
    if state == constants.ConvState.RequestVerifyExcel:
        tmp_path = constants.get_verify_path(constants.TMP_PREFIX)
        path = constants.get_verify_path()
    elif state == constants.ConvState.RequestResultExcel:
        tmp_path = constants.get_result_path(constants.TMP_PREFIX)
        path = constants.get_result_path()
    else:
        raise Exception(f"Invalid file upload state: {state}")

    await update.effective_message.reply_text(
        "File received. Please wait while I process it..."
    )
    file = await update.message.document.get_file()
    await file.download_to_drive(tmp_path)

    error = excel.validate_file(tmp_path)
    if error:
        await update.effective_message.reply_text(
            f"Unable to parse file (Error: {error}). Please try again."
        )
        return constants.ConvState.RequestVerifyExcel

    shutil.copy(tmp_path, path)

    await update.effective_message.reply_text("File processed successfully.")
    return ConversationHandler.END
