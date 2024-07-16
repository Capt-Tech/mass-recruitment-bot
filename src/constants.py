from enum import Enum
from config import config

TMP_PREFIX = "tmp_"

class ConvState(str, Enum):
    RequestInterviewExcel = "RequestInterviewExcel"
    RequestResultExcel = "RequestResultExcel"


def get_interview_path(prefix=""):
    return config.get("BASE_PATH") + "/"+prefix+"interview.csv"


def get_result_path(prefix=""):
    return config.get("BASE_PATH") + "/"+prefix+"result.csv"


START_PART_A = "Welcome to the CAPT Mass Recruitment Bot! This bot is used to manage the mass recruitment process for CAPT. You can use the following commands:\n/start - Display this message\n/interview - Get interview booking links\n/result - Get roles offered"
START_PART_B = "\n\nAdmin commands:\n/upload_interview - Upload interview schedule\n/upload_result - Upload results"

def get_start_message(is_admin):
    START_PART_C = f"\n\nPlease contact admins regarding any issues or queries:\n{"\n".join(map(lambda x: "@"+x,config.get("ADMIN_USERNAME")))}\n\nThis bot was developed by {" ".join(map(lambda x: "@"+x,config.get("DEVELOPERS")))}.\n"
#     START_PART_C = (
#     f"\n\nPlease contact admins regarding any issues or queries:\n"
#     f"{chr(10).join(map(lambda x: '@' + x, config.get('ADMIN_USERNAME')))}\n\n"
#     f"This bot was developed by {' '.join(map(lambda x: '@' + x, config.get('DEVELOPERS')))}.\n"
# )

    return START_PART_A + (START_PART_B if is_admin else "") + START_PART_C


def get_username_not_found_error_msg():
#     ERROR_MESSAGE = (
#     f"Hi! It appears we can’t find you in the system.\n\n"
#     f"Please confirm the Telegram handle you provided is correct. "
#     f"Your data may still be processing.\n\n"
#     f"If this is unexpected, please contact an admin:\n"
#     f"{chr(10).join(map(lambda x: '@' + x, config.get('ADMIN_USERNAME')))}"
# )
#     return ERROR_MESSAGE
    return f"Hi! It appears we can’t find you in the system.\n\nPlease confirm the Telegram handle you provided is correct. Your data may still be processing.\n\nIf this is unexpected, please contact an admin:\n{"\n".join(map(lambda x: "@"+x,config.get("ADMIN_USERNAME")))}"
