from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest, GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from dotenv import load_dotenv
import os

load_dotenv()

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
group1_username = 'GROUP1'  # replace with actual group1 username
group2_username = 'GROUP2'  # replace with actual group2 username

client = TelegramClient('anon', api_id, api_hash)

async def get_group_members(group):
    limit = 50 # Telegram limits how many users you can add to a group per day, which is usually around 50. So this process might take several days if you have a lot of users to add into another group.
    all_participants = []
    offset = 0
    filter = ChannelParticipantsSearch('')
    while True:
        participants = await client(GetParticipantsRequest(group, filter, offset, limit, hash=0))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset += len(participants.users)
    return all_participants

async def add_users_to_group(group, users):
    with open("failed_users.log", "a") as log_file:   # Open the log file in append mode
        for user in users:
            try:
                await client(InviteToChannelRequest(group, [user]))
            except Exception as e:
                print(f"Couldn't add {user.id} to group due to: {e}")
                log_file.write(f"{user.id}, {e}\n")   # Write user ID and error to the log file


with client:
    client.start()
    group1_members = client.loop.run_until_complete(get_group_members(group1_username))
    group2_members = client.loop.run_until_complete(get_group_members(group2_username))
    
    # We compare using user IDs as those are unique for each user
    group1_member_ids = set(user.id for user in group1_members)
    group2_member_ids = set(user.id for user in group2_members)

    missing_member_ids = group1_member_ids - group2_member_ids
    missing_members = [user for user in group1_members if user.id in missing_member_ids]
    
    # Invite missing members to group 2, in chunks of 200 users max (due to Telegram limits)
    for i in range(0, len(missing_members), 200):
        client.loop.run_until_complete(add_users_to_group(group2_username, missing_members[i:i+200]))
