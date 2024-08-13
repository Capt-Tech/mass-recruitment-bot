import constants
import pandas as pd
import json

TELEGRAM_HANDLE_COLUMN = "Telegram Handle"
COMMITTEE_COLUMN = "Committees Interested In"
PD_HANDLE_ROW = "pd"


def validate_file(path):
    is_verify_path = path == constants.get_verify_path(constants.TMP_PREFIX)
    is_result_path = path == constants.get_result_path(constants.TMP_PREFIX)

    if not is_verify_path and not is_result_path:
        return "Invalid file path"

    try:
        df = pd.read_csv(path, index_col=TELEGRAM_HANDLE_COLUMN, encoding="ISO-8859-1")

        if is_verify_path:
            try:
                df[[COMMITTEE_COLUMN]]
            except KeyError:
                return COMMITTEE_COLUMN + " column not found"

        if is_result_path:
            try:
                df.loc[PD_HANDLE_ROW]
            except KeyError:
                return PD_HANDLE_ROW + " row not found"
    except KeyError:
        return TELEGRAM_HANDLE_COLUMN + " column not found"


def get_verify_data(username: str):
    username = username.lower().strip()
    try:
        df = pd.read_csv(
            constants.get_verify_path(),
            index_col=TELEGRAM_HANDLE_COLUMN,
            encoding="ISO-8859-1",
        )
        df.index = df.index.str.lower().str.strip()
        try:
            return json.loads(df.loc[username][COMMITTEE_COLUMN])
        except KeyError:
            return []
    except FileNotFoundError:
        return []


def get_result_data(username: str):
    username = username.lower().strip()
    try:
        df = pd.read_csv(
            constants.get_result_path(),
            index_col=TELEGRAM_HANDLE_COLUMN,
            encoding="ISO-8859-1",
        )
        df.index = df.index.str.lower().str.strip()
        df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
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
        df = pd.read_csv(
            constants.get_result_path(),
            index_col=TELEGRAM_HANDLE_COLUMN,
            encoding="ISO-8859-1",
        )
        df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
        usernames_with_at = list(
            filter(
                lambda x: type(x) == str and x != PD_HANDLE_ROW and len(x.strip()) > 0,
                df.index.values.tolist(),
            )
        )
        return list(map(lambda x: x[1:], usernames_with_at))
    except FileNotFoundError:
        return None
