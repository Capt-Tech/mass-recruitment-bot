import os, json
import constants
import logging

logger = logging.getLogger("file")


def ensure_directory_exists(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)


def read_user_details(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as file:
                content = file.read().strip()
                if content:
                    return json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.error(
                f"Error reading JSON file: {e}. Initializing with an empty list."
            )
    return {}


def record_user_details(username: str, chat_id: int):
    file_path = constants.get_user_details_path()
    ensure_directory_exists(file_path)

    user_details = read_user_details(file_path)
    user_details[username.lower().strip()] = {"chat_id": chat_id}

    # Convert all keys to lowercase and strip whitespace
    user_details = {key.lower().strip(): value for key, value in user_details.items()}

    # Write the updated user details back to the JSON file
    try:
        with open(file_path, "w") as file:
            json.dump(user_details, file, indent=4)
    except Exception as e:
        logger.error(f"Error writing to JSON file: {e}")
