import constants
import pandas as pd

TELEGRAM_HANDLE_COLUMN = "telegram handle"
BOOKING_LINK_ROW = "bookingLink"
PD_HANDLE_ROW = "pd"


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
                if df.loc[username][subcomm] == "1":
                    result.append((subcomm, link))
            return result
        except KeyError:
            return []
    except FileNotFoundError:
        return []
