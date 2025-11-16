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

## Scheduling the Script on Linux

To make the library rotation happen automatically, you can use `cron`, the standard Linux task scheduler.

1.  **Open your Crontab:**
    Open a terminal on your Linux server and run the following command to edit your user's crontab file:
    ```sh
    crontab -e
    ```
    If it's your first time, you may be asked to choose a text editor (like `nano`).

2.  **Add the Schedule:**
    Add the following line to the end of the file. This example runs the script every day at 3:00 AM.

    ```cron
    0 3 * * * /usr/bin/python3 /path/to/your/rotate_jellyfin_libraries.py
    ```

    - `0 3 * * *` is the schedule (minute, hour, day of month, month, day of week).
    - `/usr/bin/python3` is the path to your Python interpreter. You can find it by running `which python3`.
    - `/path/to/your/rotate_jellyfin_libraries.py` is the absolute path to the script. Make sure the `.env` file is in the same directory.

3.  **Save and Exit:**
    - If using `nano`, press `Ctrl+X`, then `Y`, then `Enter`.

The script will now run automatically on the schedule you defined, rotating the visible libraries for your specified Jellyfin user.
