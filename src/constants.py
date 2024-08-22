from enum import Enum
from config import config

FIXED = 'fixed'
CUSTOM = 'custom'
YES = 'yes'
NO = 'no'

TMP_PREFIX = "tmp_"

MUTEX_COMMS = {"ACE" : ["CAPT in Silence PD", "CAPT in the Dark PD", "Constellations PD", "ACE Elderly PD", "ACE Homes PD", "Kindle PD", "ACE Migrants PD", "PACE PD"," Stella PD"],
             "EXA" : [ "Committee Member (10)", "Publicity Head (1)", "General Secretary (1)", "Finance Secrtary (1)"],
             "SI" : ["Committee Member (20)"],
             "Clubs & Societies" : ["General Secretary (1)", "Financial Secretary (1)", "Publicity Head (1)", "Events Executive (2)","Publicity Members (2)"],
             "Pubs" : ["CAPTlet - Journalism Head", "CAPTlet - Designer Head", "CAPTlet - Journalist (2)"," CAPTlet - Designer (2)", "Design - Board Design Head", "Design - Merchandise Head", "Design Member (4)", "Socials - Social Media Head", "Socials - Events Coverage Head", "Socials - Social Media Content Creator (3)", "Socials - Events Coverage Specialist (2)", "TechDev - CAPTlife Head", "TechDev - Treeckle Head", "TechDev Developer (5)"],
             "Sports Committee" : ["General Secretary", "EXCO role (1)", "Financial Secretary", "Sub-comm role (1)", "Events IC", "Sub-comm role (2)" ,"Publicity IC", "Sub comm role (2)" ],
             "SAC" : ["General Secretary (1)", "Finance Secretary (1)", "Publicity Head (1)", "Welfare Executive (2)" ,"Welcome Back Dinner (WBD) Executive (2)" ,"CAPTain Meets Baegel (CMB) Executive (2)","Inter-Neighbourhood Shield (INS) Executive (2)","CAPT Buddy Executive (1)"],
             "FOC" : ["Project Director (1)"],
             "Rag & Flag" : ["Project Director (1)"],
             "CE Fest 2024" : ["Project Director (1)"],
             "Roc House Comm" : ["Programmes (6)", "Publicity (6)", "Admin and Finance Secrataries (4)"],
             "Dragon House Comm" : ["Secretaries (Finance) (1)", "Secretaries (General) (1)", "Creatives (4)", "Events (4)", "Welfare (3)"],
             "Garuda House Comm" : ["Admin & Finance members (3)", "Programmes members (6)", "Publicity members (4)"," Tech members (2)"],
             "Pheonix House Comm" : ["Welfare (5)", "Spirits (5)", "Socials & Designs (5)", "General Secretary (1)", "Finance Secretary (1)"],
             "Tulpar House Comm" : ["Events/Welfare (8)", "Pubs (3)", "Admin/Fin (3)"]
}

class ConvState(str, Enum):
    RequestVerifyExcel = "RequestVerifyExcel"
    RequestResultExcel = "RequestResultExcel"
    Choosing = "Choosing"
    WaitingPhoto = "WaitingPhoto"
    TypingReply = "TypingReply"
    ConfirmBroadcast = "Confirm"

class BroadcastType(str, Enum):
    Message = "BroadcastMessage"
    Results = "BroadcastResults"

def get_verify_path(prefix=""):
    return config.get("BASE_PATH") + "/"+prefix+"verify.csv"


def get_result_path(prefix=""):
    return config.get("BASE_PATH") + "/"+prefix+"result.csv"


def get_user_details_path(prefix=""):
    return config.get("BASE_PATH") + "/"+prefix+"user_details.json"

COMMANDS = {
    "start": "Display help page",
    "verify": "Verify the committees you applied to",
    "result": "Get roles offered",
}

ADMIN_COMMANDS = {
    "upload_verify": "Upload verification data",
    "upload_result": "Upload results",
    "broadcast_message": "Broadcast a message to all users",
    "broadcast_results": "Broadcast results to all users",
    "registered_users": "List all registered users",
}

START_PART_A = "Welcome to the CAPT Mass Recruitment Bot! This bot is used to manage the mass recruitment process for CAPT. You can use the following commands:\n" + "\n".join(map(lambda x: f"/{x} - {COMMANDS[x]}",COMMANDS.keys()))
START_PART_B = "\n\nAdmin commands:\n" + "\n".join(map(lambda x: f"/{x} - {ADMIN_COMMANDS[x]}",ADMIN_COMMANDS.keys()))

def get_start_message(is_admin):
    START_PART_C = f"\n\nPlease contact admins regarding any issues or queries:\n{"\n".join(map(lambda x: "@"+x,config.get("ADMIN_USERNAME")))}\n\nThis bot was developed by {" ".join(map(lambda x: "@"+x,config.get("DEVELOPERS")))}.\n"
    return START_PART_A + (START_PART_B if is_admin else "") + START_PART_C


def get_username_not_found_error_msg():
    return f"Hi! It appears we can’t find you in the system.\n\nPlease confirm the Telegram handle you provided is correct. Your data may still be processing.\n\nIf this is unexpected, please contact an admin:\n{"\n".join(map(lambda x: "@"+x,config.get("ADMIN_USERNAME")))}"


