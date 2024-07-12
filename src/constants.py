from enum import Enum
from config import config


class ConvState(str, Enum):
    RequestInterviewExcel = "RequestInterviewExcel"


def get_interview_path():
    return config.get("BASE_PATH") + "/interview.csv"
