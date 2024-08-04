import os, json
import constants

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
            print(f"Error reading JSON file: {e}. Initializing with an empty list.")
    return {}

def record_user_details(username, chat_id):
    file_path = constants.get_user_details_path()
    ensure_directory_exists(file_path)

    user_details = read_user_details(file_path)
    user_details[username] = {"chat_id": chat_id}

    # Write the updated user details back to the JSON file
    try:
        with open(file_path, "w") as file:
            json.dump(user_details, file, indent=4)
        print("Details recorded successfully.")
    except Exception as e:
        print(f"Error writing to JSON file: {e}")

