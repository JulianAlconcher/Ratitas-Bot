import discord
from config import DISCORD_BOT_TOKEN, DISCORD_CHANNEL_ID
import asyncio
import time

BOT_TOKEN = DISCORD_BOT_TOKEN
CHANNEL_ID_STR = DISCORD_CHANNEL_ID

if not BOT_TOKEN or not CHANNEL_ID_STR or BOT_TOKEN == "YOUR_BOT_TOKEN" or CHANNEL_ID_STR == "YOUR_CHANNEL_ID":
    print("Error: Please set your actual DISCORD_BOT_TOKEN and DISCORD_CHANNEL_ID in the config.py file.")
    exit()

try:
    CHANNEL_ID = int(CHANNEL_ID_STR)
except (ValueError, TypeError):
    print("Error: DISCORD_CHANNEL_ID must be a valid integer in config.py.")
    exit()

intents = discord.Intents.default()
intents.presences = True
intents.members = True

client = discord.Client(intents=intents)

last_mobile_alert = {}

MIN_INTERVAL = 3600 

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_presence_update(before, after):
    if not after.bot and after.is_on_mobile():
        now = time.time()
        last_alert = last_mobile_alert.get(after.id, 0)

        if now - last_alert >= MIN_INTERVAL:
            channel = client.get_channel(CHANNEL_ID)
            if channel:
                await channel.send(f'{after.name} Mirala a la ratita entrando desde el celu...')
            last_mobile_alert[after.id] = now

if BOT_TOKEN:
    client.run(BOT_TOKEN)
else:
    print("Error: DISCORD_BOT_TOKEN environment variable not set.")
