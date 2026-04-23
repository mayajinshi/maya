import os
import asyncio
import random
import time
from datetime import datetime
from threading import Thread
from flask import Flask

from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from openai import OpenAI

# ---------------- WEB SERVER ---------------- #

app = Flask('')

@app.route('/')
def home():
    return "adubot is alive"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    Thread(target=run).start()

# ---------------- TELEGRAM CLIENT ---------------- #

api_id = 39905812
api_hash = "47c868709156df4c03c3c40c8b78518c"
session = "1BVtsOLoBuy0znlRIx7OYESvSkzisDcItDVMop-NxEkPSZmGfYccQJebiiXg3vyvSIec3GPPieLBbKSEzfwLFhKMbdzx68jQjxXR3M_JBURWrCOxnkFlMNQt1EhYk0s_g1LNLEasFD7ZpzOjGUHwH3Ch4bH9iSOIhfg8RtU7xBOK086TMWMt6t8sBvt-wZ2LzCb1q68fOhA0ksR81aOZ2GZm4F7Xjb1ZoIZiBTU35G9r2xeoGGzpvL5FuETfnZ7h_XhFZmPco_l19ZoEViUsxEiMC2qL03i6vLZ5Zd1txQakeLVxT25o_3xpkrsAjaIFinBzSQSNifWlP8sbc-gKVxPBwWQ_rO2w="

client = TelegramClient(StringSession(session), api_id, api_hash)

TARGET_GROUP_ID = -1003623091628
replied_users = set()
start_time = time.time()

GROUP_LINK = "@WIFE_SWAPPING_GF"


quotes = ["Hi", "Hii", "Addd Mee", "Heloo", "Nice"]

# ---------------- AUTO GROUP QUOTES ---------------- #

async def send_quotes():
    while True:
        for dialog in await client.get_dialogs():
            if dialog.is_group:
                try:
                    await client.send_message(dialog.id, random.choice(quotes))
                    await asyncio.sleep(10)
                except:
                    pass
        await asyncio.sleep(300)

# ---------------- PRIVATE AUTO REPLY ---------------- #

@client.on(events.NewMessage(incoming=True))
async def private_auto_reply(event):
    if event.is_private and not event.out:
        user_id = event.sender_id

        if user_id not in replied_users:
            replied_users.add(user_id)

            await asyncio.sleep(2)

            await event.respond(
                f"Hello dear ❤️\n\n"
                f"Thanks for messaging.\n"
                f"Please join our group here:\n{GROUP_LINK}\n\n"
                f"After joining, message me again 💋"
            )

# ---------------- SIMPLE PRIVATE KEYWORDS ---------------- #

@client.on(events.NewMessage(incoming=True, pattern=r'(?i)^demo$'))
async def demo_reply(event):
    if event.is_private:
        await event.reply("demo paid hai babe.. 100rs only")

# ---------------- COMMANDS ---------------- #

@client.on(events.NewMessage(outgoing=True, pattern=r"\.ping"))
async def ping(event):
    start = time.time()
    msg = await event.edit("𝙋𝙞𝙣𝙜𝙞𝙣𝙜...")
    end = time.time()
    await msg.edit(f"𝗣𝗢𝗡𝗚! {round((end-start)*1000)} ms")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.id"))
async def get_id(event):
    await event.edit(f"𝘾𝙃𝘼𝙏 𝙄𝘿: `{event.chat_id}`")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.time"))
async def time_cmd(event):
    now = datetime.now().strftime("%H:%M:%S")
    await event.edit(f"𝘾𝙐𝙍𝙍𝙀𝙉𝙏 𝙏𝙄𝙈𝙀: {now}")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.alive"))
async def alive(event):
    uptime = int(time.time() - start_time)
    await event.edit(f"⚡ 𝙕𝙄𝙉𝘿𝘼 𝙃𝙐...\nUptime: {uptime} sec")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.block"))
async def block_user(event):
    if event.is_private:
        await client(BlockRequest(event.chat_id))
        await event.edit("Blocked.")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.unblock"))
async def unblock_user(event):
    if event.is_private:
        await client(UnblockRequest(event.chat_id))
        await event.edit("User unblocked.")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.spam (.+)"))
async def spam(event):
    args = event.raw_text.split(maxsplit=2)
    count = int(args[1])
    text = args[2]
    await event.delete()

    for _ in range(count):
        await client.send_message(event.chat_id, text)


# ---------------- MAIN ---------------- #

async def main():
    await client.start()
    print("Userbot running...")

    asyncio.create_task(send_quotes())

    await client.run_until_disconnected()

keep_alive()
asyncio.run(main())
