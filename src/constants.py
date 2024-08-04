from enum import Enum
from config import config

FIXED = 'fixed'
CUSTOM = 'custom'
YES = 'yes'
NO = 'no'

TMP_PREFIX = "tmp_"

class ConvState(str, Enum):
    RequestInterviewExcel = "RequestInterviewExcel"
    RequestResultExcel = "RequestResultExcel"
    Choosing = "Choosing"
    TypingReply = "TypingReply"
    ConfirmBroadcast = "Confirm"

class BroadcastType(str, Enum):
    Message = "BroadcastMessage"
    Results = "BroadcastResults"

def get_interview_path(prefix=""):
    return config.get("BASE_PATH") + "/"+prefix+"interview.csv"


def get_result_path(prefix=""):
    return config.get("BASE_PATH") + "/"+prefix+"result.csv"


def get_user_details_path(prefix=""):
    return config.get("BASE_PATH") + "/"+prefix+"user_details.json"


START_PART_A = "Welcome to the CAPT Mass Recruitment Bot! This bot is used to manage the mass recruitment process for CAPT. You can use the following commands:\n/start - Display this message\n/interview - Get interview booking links\n/result - Get roles offered"
START_PART_B = "\n\nAdmin commands:\n/upload_interview - Upload interview schedule\n/upload_result - Upload results\n/broadcast_message - Broadcast a message to all users\n/broadcast_results - Broadcast results to all users"

def get_start_message(is_admin):
    START_PART_C = f"\n\nPlease contact admins regarding any issues or queries:\n{"\n".join(map(lambda x: "@"+x,config.get("ADMIN_USERNAME")))}\n\nThis bot was developed by {" ".join(map(lambda x: "@"+x,config.get("DEVELOPERS")))}.\n"
    return START_PART_A + (START_PART_B if is_admin else "") + START_PART_C


def get_username_not_found_error_msg():
    return f"Hi! It appears we can’t find you in the system.\n\nPlease confirm the Telegram handle you provided is correct. Your data may still be processing.\n\nIf this is unexpected, please contact an admin:\n{"\n".join(map(lambda x: "@"+x,config.get("ADMIN_USERNAME")))}"


