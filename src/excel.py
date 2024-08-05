import constants
import pandas as pd
import math

TELEGRAM_HANDLE_COLUMN = "telegram handle"
BOOKING_LINK_ROW = "bookingLink"
PD_HANDLE_ROW = "pd"

INTERVIEW_POSITIVE = "1"


def validate_interview_file(path):
    is_interview_path = path == constants.get_interview_path(constants.TMP_PREFIX)
    is_result_path = path == constants.get_result_path(constants.TMP_PREFIX)

    if not is_interview_path and not is_result_path:
        return "Invalid file path"

    try:
        df = pd.read_csv(path, index_col=TELEGRAM_HANDLE_COLUMN)

        if is_interview_path:
            try:
                df.loc[BOOKING_LINK_ROW]
            except KeyError:
                return BOOKING_LINK_ROW + " row not found"

        if is_result_path:
            try:
                df.loc[PD_HANDLE_ROW]
            except KeyError:
                return PD_HANDLE_ROW + " row not found"
    except KeyError:
        return TELEGRAM_HANDLE_COLUMN + " column not found"


def get_interview_data(username):
    try:
        df = pd.read_csv(
            constants.get_interview_path(), index_col=TELEGRAM_HANDLE_COLUMN
        )
        links = df.loc[BOOKING_LINK_ROW].items()
        try:
            result = []
            for subcomm, link in links:
                if df.loc[username][subcomm] == INTERVIEW_POSITIVE:
                    result.append((subcomm, link))
            return result
        except KeyError:
            return []
    except FileNotFoundError:
        return []


def get_result_data(username):
    try:
        df = pd.read_csv(constants.get_result_path(), index_col=TELEGRAM_HANDLE_COLUMN)
        pd_handles = df.loc[PD_HANDLE_ROW].items()
        try:
            result = []
            for comm, handle in pd_handles:
                subcomm = df.loc[username][comm]
                if not subcomm or type(subcomm) != str:
                    continue
                subcomm = subcomm.strip()
                if len(subcomm) > 0:
                    result.append((comm, subcomm, handle))
            return result
        except KeyError:
            return None
    except FileNotFoundError:
        return None


def get_result_usernames():
    try:
        df = pd.read_csv(constants.get_result_path(), index_col=TELEGRAM_HANDLE_COLUMN)
        usernames_with_at = list(
            filter(lambda x: x != PD_HANDLE_ROW, df.index.values.tolist())
        )
        return list(map(lambda x: x[1:], usernames_with_at))
    except FileNotFoundError:
        return None
