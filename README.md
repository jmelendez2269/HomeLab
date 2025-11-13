# Jellyfin Library Rotator

This script rotates the visible libraries (categories) for a specific Jellyfin user. It randomly selects a specified number of libraries from all available libraries and updates the user's access policy to make only the selected libraries visible.

This is useful for creating a dynamic, ever-changing home screen for a user, preventing the same categories from always being displayed.

## How It Works

The script uses the Jellyfin API to perform the following actions:
1.  Fetches all available libraries on your Jellyfin server.
2.  Randomly selects a subset of these libraries.
3.  Updates the access policy for a specified user to grant access only to the selected libraries.

## Prerequisites

- Python 3.6+
- The `requests` and `python-dotenv` Python libraries.

## Setup and Configuration

1.  **Install Python Libraries:**
    Open a terminal or PowerShell and run the following command to install the necessary libraries:
    ```sh
    pip install requests python-dotenv
    ```

2.  **Create a `.env` file:**
    In the same directory as the `rotate_jellyfin_libraries.py` script, create a file named `.env`. This file will store your configuration details securely.

3.  **Add Configuration to `.env` file:**
    Open the `.env` file and add the following lines, replacing the placeholder values with your actual Jellyfin server details:

    ```env
    # The full URL of your Jellyfin server
    JELLYFIN_SERVER_URL="http://localhost:8096"

    # An API key with administrative privileges.
    # You can generate this in your Jellyfin Dashboard under Advanced > API Keys.
    ADMIN_API_KEY="YOUR_ADMIN_API_KEY"

    # The ID of the user whose libraries you want to rotate.
    # You can find this in the URL when editing a user in the Jellyfin Dashboard.
    # For example, if the URL is .../user.html?userId=xxxxxxxx, then the string of x's is the user ID.
    USER_ID="YOUR_USER_ID"

    # The number of libraries to make visible at random.
    NUM_VISIBLE_LIBRARIES="5"
    ```

## Running the Script

You can run the script manually from a terminal or PowerShell:

```sh
python rotate_jellyfin_libraries.py
```

The script will print the libraries it has selected and confirm that the user's policy has been updated.

## Scheduling the Script on Windows

To make the library rotation happen automatically, you can use the Windows Task Scheduler.

1.  **Open Task Scheduler:**
    Press the Windows key, type "Task Scheduler", and press Enter.

2.  **Create a New Task:**
    In the right-hand pane, click "Create Basic Task...".

3.  **Name and Description:**
    - Name: `Jellyfin Library Rotator`
    - Description: `Rotates the visible libraries for a Jellyfin user on a schedule.`
    - Click `Next`.

4.  **Trigger:**
    - Choose how often you want the rotation to happen (e.g., `Daily`, `Weekly`).
    - Click `Next` and specify the time you want the task to run.

5.  **Action:**
    - Select `Start a program`.
    - Click `Next`.

6.  **Start a Program:**
    - **Program/script:** Enter the full path to your Python executable (e.g., `C:\Python39\python.exe`). You can find this by running `where python` in PowerShell.
    - **Add arguments (optional):** Enter the full path to your `rotate_jellyfin_libraries.py` script (e.g., `C:\Users\YourUser\Documents\Projects\Home Lab\rotate_jellyfin_libraries.py`).
    - **Start in (optional):** Enter the directory where your script is located (e.g., `C:\Users\YourUser\Documents\Projects\Home Lab`). This is important so the script can find the `.env` file.

7.  **Finish:**
    - Review the settings and click `Finish`.

The script will now run automatically on the schedule you defined, rotating the visible libraries for your specified Jellyfin user.
