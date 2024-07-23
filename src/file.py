import os, json
import constants





def record_user_details(username, chat_id):
    file_path = constants.get_user_details_path()
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Initialize an empty list for storing user details
    user_details = {}

    # Read existing data from the JSON file if it exists
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as file:
                content = file.read().strip()
                if content:
                    user_details = json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error reading JSON file: {e}. Initializing with an empty list.")

    user_details[username] = {"chat_id": chat_id}

    # Write the updated user details back to the JSON file
    with open(file_path, "w") as file:
        json.dump(user_details, file, indent=4)

    print("Details recorded")
