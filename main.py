import asyncio
import logging
from telethon import TelegramClient, events

# Bot credentials
API_ID = 28507153  # Replace with your API ID
API_HASH = "68391d8f84e503d36bc49f0215148b67"  # Replace with your API hash
BOT_TOKEN = "7501256326:AAHRrZa2-OtHqub_axwvBv1dvzWL8WAAc7I"  # Replace with your bot token

# Initialize the Telegram bot client
client = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Dictionary to store multiple source and destination mappings with names
channel_mappings = {}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ForwardBot")

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("✅ Bot is running! Use /setpair to configure forwarding.")

@client.on(events.NewMessage(pattern='/commands'))
async def list_commands(event):
    commands = """
    📌 Available Commands:
    /setpair <name> <source> <destination> - Add a forwarding pair
    /listpairs - List all forwarding pairs
    /pausepair <name> - Pause a forwarding pair
    /startpair <name> - Resume a forwarding pair
    /clearpairs - Clear all forwarding pairs
    """
    await event.reply(commands)

@client.on(events.NewMessage(pattern='/setpair (.+) (.+) (.+)'))
async def set_pair(event):
    pair_name = event.pattern_match.group(1)
    source = event.pattern_match.group(2)
    destination = event.pattern_match.group(3)
    user_id = event.sender_id

    if user_id not in channel_mappings:
        channel_mappings[user_id] = {}
    channel_mappings[user_id][pair_name] = {'source': source, 'destination': destination, 'active': True}

    await event.reply(f"✅ Forwarding pair '{pair_name}' added: {source} → {destination}")

@client.on(events.NewMessage(pattern='/listpairs'))
async def list_pairs(event):
    user_id = event.sender_id
    if user_id in channel_mappings and channel_mappings[user_id]:
        pairs_list = "\n".join([f"{name}: {data['source']} → {data['destination']} (Active: {data['active']})" for name, data in channel_mappings[user_id].items()])
        await event.reply(f"📋 Active Forwarding Pairs:\n{pairs_list}")
    else:
        await event.reply("⚠️ No forwarding pairs found.")

@client.on(events.NewMessage(pattern='/pausepair (.+)'))
async def pause_pair(event):
    pair_name = event.pattern_match.group(1)
    user_id = event.sender_id
    if user_id in channel_mappings and pair_name in channel_mappings[user_id]:
        channel_mappings[user_id][pair_name]['active'] = False
        await event.reply(f"⏸️ Forwarding pair '{pair_name}' paused.")
    else:
        await event.reply("⚠️ Pair not found.")

@client.on(events.NewMessage(pattern='/startpair (.+)'))
async def start_pair(event):
    pair_name = event.pattern_match.group(1)
    user_id = event.sender_id
    if user_id in channel_mappings and pair_name in channel_mappings[user_id]:
        channel_mappings[user_id][pair_name]['active'] = True
        await event.reply(f"▶️ Forwarding pair '{pair_name}' resumed.")
    else:
        await event.reply("⚠️ Pair not found.")

@client.on(events.NewMessage(pattern='/clearpairs'))
async def clear_pairs(event):
    user_id = event.sender_id
    if user_id in channel_mappings:
        del channel_mappings[user_id]
        await event.reply("🗑️ All forwarding pairs have been cleared!")
    else:
        await event.reply("⚠️ No forwarding pairs were found.")

@client.on(events.NewMessage)
async def forward_messages(event):
    user_id = event.sender_id
    if user_id in channel_mappings:
        for pair_name, mapping in channel_mappings[user_id].items():
            if mapping['active'] and event.chat_id == int(mapping['source']):
                await client.send_message(int(mapping['destination']), event.message)

async def main():
    print("🚀 Bot is running! Use /setpair to configure forwarding.")
    await client.run_until_disconnected()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
