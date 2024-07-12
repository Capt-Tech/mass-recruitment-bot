from enum import Enum
from config import config


class ConvState(str, Enum):
    RequestInterviewExcel = "RequestInterviewExcel"
    RequestResultExcel = "RequestResultExcel"


def get_interview_path():
    return config.get("BASE_PATH") + "/interview.csv"


def get_result_path():
    return config.get("BASE_PATH") + "/result.csv"


START_PART_A = "Welcome to the CAPT Mass Recruitment Bot! This bot is used to manage the mass recruitment process for CAPT. You can use the following commands:\n/start - Display this message\n/interview - Get interview booking links\n/result - Get roles offered"
START_PART_B = "\n\nAdmin commands:\n/upload_interview - Upload interview schedule\n/upload_result - Upload results"

def get_start_message(is_admin):
    START_PART_C = f"\n\nPlease contact admins regarding any issues or queries:\n{"\n".join(map(lambda x: "@"+x,config.get("ADMIN_USERNAME")))}\n\nThis bot was developed by {" ".join(map(lambda x: "@"+x,config.get("DEVELOPERS")))}.\n"
    return START_PART_A + (START_PART_B if is_admin else "") + START_PART_C
