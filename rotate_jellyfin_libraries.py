```

import requests
import json
import random
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
# Get from .env file or set them directly
JELLYFIN_SERVER_URL = os.getenv("JELLYFIN_SERVER_URL", "http://localhost:8096")
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "YOUR_ADMIN_API_KEY")
USER_ID = os.getenv("USER_ID", "YOUR_USER_ID")
NUM_VISIBLE_LIBRARIES = int(os.getenv("NUM_VISIBLE_LIBRARIES", "5")) # Number of libraries to make visible at random

def get_all_libraries(headers):
    """Fetches all available libraries from the Jellyfin server."""
    print("Fetching all libraries...")
    try:
        response = requests.get(f"{JELLYFIN_SERVER_URL}/Library/VirtualFolders", headers=headers)
        response.raise_for_status()
        all_libraries = response.json()
        print(f"Found {len(all_libraries)} libraries.")
        return {library["Name"]: library["ItemId"] for library in all_libraries}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching libraries: {e}")
        return None

def get_user_policy(headers):
    """Fetches the current policy for the specified user."""
    print(f"Fetching current policy for user ID: {USER_ID}...")
    try:
        response = requests.get(f"{JELLYFIN_SERVER_URL}/Users/{USER_ID}", headers=headers)
        response.raise_for_status()
        user_data = response.json()
        print("Current user policy fetched.")
        return user_data.get("Policy", {})
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user policy: {e}")
        return None

def update_user_policy(headers, new_policy):
    """Updates the user's policy on the Jellyfin server."""
    print(f"Updating policy for user ID: {USER_ID}...")
    try:
        response = requests.post(
            f"{JELLYFIN_SERVER_URL}/Users/{USER_ID}/Policy",
            headers=headers,
            json=new_policy,
        )
        response.raise_for_status()
        print("User policy updated successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error updating user policy: {e}")
        if response:
            print(f"Response content: {response.text}")

def rotate_libraries():
    """
    Rotates the visible libraries for a user by randomly selecting a subset of libraries
    and updating the user's access policy.
    """
    headers = {
        "X-Emby-Token": ADMIN_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    library_name_to_id = get_all_libraries(headers)
    if not library_name_to_id:
        return

    current_policy = get_user_policy(headers)
    if not current_policy:
        return

    # Get all library names and randomly select a subset
    all_library_names = list(library_name_to_id.keys())
    if len(all_library_names) <= NUM_VISIBLE_LIBRARIES:
        print("Number of visible libraries is greater than or equal to the total number of libraries.")
        print("All libraries will be made visible.")
        selected_libraries = all_library_names
    else:
        selected_libraries = random.sample(all_library_names, NUM_VISIBLE_LIBRARIES)

    print(f"\nSelected libraries to be visible: {', '.join(selected_libraries)}")

    # Create the new policy
    new_policy = current_policy.copy()
    new_policy["EnableAllFolders"] = False
    new_policy["EnabledFolders"] = [library_name_to_id[name] for name in selected_libraries]

    # Ensure BlockedFolders is not used if EnabledFolders is being managed
    if "BlockedFolders" in new_policy:
        del new_policy["BlockedFolders"]

    update_user_policy(headers, new_policy)

if __name__ == "__main__":
    if ADMIN_API_KEY == "YOUR_ADMIN_API_KEY" or USER_ID == "YOUR_USER_ID":
        print("Please configure your JELLYFIN_SERVER_URL, ADMIN_API_KEY, and USER_ID in a .env file or directly in the script.")
    else:
        rotate_libraries()

```