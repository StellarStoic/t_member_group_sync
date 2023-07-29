# Telegram Group Member Sync Between Two Groups

This is a simple Python script using the [Telethon](https://github.com/LonamiWebs/Telethon) library for syncing members between two Telegram groups.

## Requirements

- Python 3.6 or higher
- Python packages: `telethon`, `python-dotenv`

## Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Copy the `.env.sample` to `.env`:
   ```
   cp .env.sample .env
   ```

4. Fill in the `TELEGRAM_API_ID` and `TELEGRAM_API_HASH` variables in the `.env` file. You can get these values from [My Telegram](https://my.telegram.org/).

5. Fill in the `GROUP1` and `GROUP2` variables in the script file with the usernames of the Telegram groups that you want to sync members between.

## Usage

1. Run the script:
   ```
   python script.py
   ```

This script will first fetch all members from the two Telegram groups. Then, it will find the members that are in the first group but not in the second group. These "missing" members will be added to the second group. 

Due to Telegram's limits, the script can only add around 50 members per day to a group. If you have more than 50 members to add, you will need to run the script across multiple days.

If the script is unable to add a user to the second group (for example, because of the user's privacy settings), the user's ID and the error message will be logged in the `failed_users.log` file.