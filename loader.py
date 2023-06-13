from pyrogram import Client
import os
from config import API_ID, API_HASH, BOT_TOKEN
app = Client(
    "my_bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

os.system('cls')
print('Ok im working')
