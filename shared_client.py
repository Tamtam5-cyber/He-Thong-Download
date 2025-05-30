from telethon import TelegramClient
from config import API_ID, API_HASH, BOT_TOKEN, STRING
from pyrogram import Client
import sys
import re

# Kiểm tra định dạng BOT_TOKEN
def validate_bot_token(token):
    if not token:
        return False
    # Kiểm tra định dạng token: <number>:<string>
    pattern = r'^\d+:[A-Za-z0-9_-]{35}$'
    return bool(re.match(pattern, token))

client = TelegramClient("telethonbot", API_ID, API_HASH)
app = Client("pyrogrambot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
userbot = Client("4gbbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING)

async def start_client():
    # Kiểm tra BOT_TOKEN
    if not validate_bot_token(BOT_TOKEN):
        print("Error: Invalid BOT_TOKEN. Please check your config.py.")
        sys.exit(1)

    try:
        if not client.is_connected():
            await client.start(bot_token=BOT_TOKEN)
            print("SpyLib started...")
    except Exception as e:
        print(f"Error starting Telethon client: {e}")
        sys.exit(1)

    if STRING:
        try:
            await userbot.start()
            print("Userbot started...")
        except Exception as e:
            print(f"Hey honey!! Check your premium string session, it may be invalid or expired: {e}")
            sys.exit(1)

    try:
        await app.start()
        print("Pyro App Started...")
        # Kiểm tra kết nối Pyrogram
        me = await app.get_me()
        print(f"Pyrogram client connected as @{me.username}")
    except Exception as e:
        print(f"Error starting Pyrogram client: {e}")
        sys.exit(1)

    return client, app, userbot
