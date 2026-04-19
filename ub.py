import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import asyncio
import random
from flask import Flask
from threading import Thread
import time
from datetime import datetime
from openai import OpenAI
from telethon.tl.functions.contacts import BlockRequest
from telethon import events

app = Flask('')

@app.route('/')
def home():
    return "adubot is alive"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

api_id = 20900277
api_hash = "6a3d761f9be590be4259404f34a1f81e"
session = "1BVtsOIQBuyZEug8Cibrhs0DTVwNad4D_iJGVL2vtSfKra0cnCp2OoyXih6zwvaud7Jkh5WJj0ar8fOkQKuzNZZw5rRzEC5mKR2W64aFo3ZR8eLjDk3heAxXVoGOvs0S-BM3QTh6k5-CjSFOBI2p_FWQtwu2NsYb114TVijvOWPFVN7hliwQeobJ5Hh-ABSRjRbqE9cryb6H-e2-AoYi-8_cD0cwIIH4dik1IjCYMLcmbwP2Bk_ck2ydA8b9WYLeaoMtHmNowyBoJV_EKvWGi2VTKAmaNOgbN9K0g4jeJuj20EmSydKJDdNuv3ekNH1VakZF4MDmElfYVYRcbYDIrIDa29FPOq08="

client = TelegramClient(StringSession(session), api_id, api_hash)

replied_users = set()

@client.on(events.NewMessage(outgoing=True, pattern=r"\.block"))
async def block_user(event):
    if event.is_private:
        entity = await client.get_entity(event.chat_id)
        await client(BlockRequest(entity))
        await event.edit("Blocked.")


from telethon.tl.functions.contacts import UnblockRequest

@client.on(events.NewMessage(outgoing=True, pattern=r"\.unblock"))
async def unblock_user(event):
    if event.is_private:
        await client(UnblockRequest(event.chat_id))
        await event.edit("User unblocked.")

TARGET_GROUP_ID = -1003623091628

@client.on(events.ChatAction())
async def welcome_new_member(event):
    if event.chat_id == TARGET_GROUP_ID:
        if event.user_joined or event.user_added:
            user = await event.get_user()
            await client.send_message(
                TARGET_GROUP_ID,
                f"𝗪𝗘𝗟𝗖𝗢𝗠𝗘 {user.first_name} ❤️\n\n𝗠𝗘𝗦𝗦𝗔𝗚𝗘 𝗠𝗘 𝗙𝗢𝗥 𝗙𝗨𝗡 & 𝗖𝗔𝗠 𝗦𝗛𝗢𝗪. 𝗠𝗨𝗔𝗔𝗔𝗛𝗛 💋"
            )
    

@client.on(events.NewMessage(incoming=True))
async def auto_price(event):
    if event.is_private and not event.out:
        user_id = event.sender_id

        if user_id not in replied_users:
            replied_users.add(user_id)

            await asyncio.sleep(2)
            await event.respond('''🐣🦋 𝗡𝗔𝗩𝗬𝗔 𝗔𝗩𝗔𝗜𝗟𝗔𝗕𝗟𝗘 🐣🦋

       🍒  𝗩𝗢𝗜𝗖𝗘 𝗖𝗔𝗟𝗟  🍒

🍒𝟱 𝗠𝗜𝗡𝗨𝗧𝗘𝗦 - 𝟮𝟬𝟬 𝗥𝗦 💦
🍒𝟭𝟬 𝗠𝗜𝗡𝗨𝗧𝗘𝗦 - 𝟯𝟱𝟬 𝗥𝗦 💦

       🎀 𝗩𝗜𝗗𝗘𝗢 𝗖𝗔𝗟𝗟 💘

🍒𝟱 𝗠𝗜𝗡𝗨𝗧𝗘𝗦 - 𝟱𝟬𝟬 𝗥𝗦  💦
🍒𝟭𝟬 𝗠𝗜𝗡𝗨𝗧𝗘𝗦 - 𝟴𝟬𝟬 𝗥𝗦 💦

       🌟 𝗦𝗘𝗫 𝗖𝗛𝗔𝗧 👄

🍒𝟱 𝗠𝗜𝗡𝗨𝗧𝗘𝗦 - 𝟮𝟬𝟬 𝗥𝗦 💦
🍒𝟭𝟬 𝗠𝗜𝗡𝗨𝗧𝗘𝗦 - 𝟯𝟱𝟬 𝗥𝗦 💦

       🎀 𝗦𝗣𝗘𝗖𝗜𝗔𝗟 𝗦𝗛𝗢𝗪 💘

🍒 𝗦𝗔𝗥𝗘𝗘 𝗦𝗛𝗢𝗪 - 𝟭𝟮𝟬𝟬 𝗥𝗦 💦
🍒 𝗦𝗤𝗨𝗜𝗥𝗧 𝗦𝗛𝗢𝗪 - 𝟭𝟭𝟬𝟬 𝗥𝗦 💦

💟𝗗𝗘𝗠𝗢 - 𝟭𝟬𝟬 𝗥𝗦💟''')

@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    if event.is_private and not event.out:
        if event.raw_text.lower() in ["h00000i", "hel000000lo", "h000009y", "he0000009y"]:
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(random.randint(2,4))
            await event.reply(''' wait.. 2 min me aayi ❤️''')

client_ai = OpenAI(api_key="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")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.q (.+)"))
async def gpt_reply(event):
    prompt = event.pattern_match.group(1)
    await event.edit("Thinking...")

    try:
        response = client_ai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content
        await event.edit(answer)

    except Exception as e:
        await event.edit(f"Error: {e}")
        
@client.on(events.NewMessage(incoming=True))
async def auto_repl(event):
    if event.is_private and not event.out:
        if event.raw_text.lower() in ["demo"]:
            async with client.action(event.chat_id, 'typing'):
                await asyncio.sleep(random.randint(2,4))
            await event.reply(''' demo paid hai babe.. 100rs only''')

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

@client.on(events.NewMessage(outgoing=True, pattern=r"\.userinfo"))
async def userinfo(event):
    user = await event.get_sender()
    await event.edit(
        f"𝙉𝘼𝙈𝙀: {user.first_name}\n𝙄𝘿: {user.id}"
    )

@client.on(events.NewMessage(outgoing=True, pattern=r"\.del"))
async def delete(event):
    if event.reply_to_msg_id:
        msg = await event.get_reply_message()
        await msg.delete()
        await event.delete()

@client.on(events.NewMessage(outgoing=True, pattern=r"\.help"))
async def help_cmd(event):
    await event.edit("""
𝙇𝙄𝙎𝙏 𝙊𝙁 𝙑𝘼𝙇𝙄𝘿 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎:
• .ping - test
• .id - int id number
• .time - time
• .userinfo - information
• .del - delete
• .help - assist
• .spam - spamming
• .boost - boost link
• .alive - run
• .pay - pay
• .rl - rate list
• .block - block user
• .unblock - unblock user
• .q - ask chatgpt
""")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.rl"))
async def help_cmd(event):
    await event.edit(""" 🐣🦋 𝗡𝗔𝗩𝗬𝗔 𝗔𝗩𝗔𝗜𝗟𝗔𝗕𝗟𝗘 🐣🦋

       🍒  𝗩𝗢𝗜𝗖𝗘 𝗖𝗔𝗟𝗟  🍒

🍒𝟱 𝗠𝗜𝗡𝗨𝗧𝗘𝗦 - 𝟮𝟬𝟬 𝗥𝗦 💦
🍒𝟭𝟬 𝗠𝗜𝗡𝗨𝗧𝗘𝗦 - 𝟯𝟱𝟬 𝗥𝗦 💦

       🎀 𝗩𝗜𝗗𝗘𝗢 𝗖𝗔𝗟𝗟 💘

🍒𝟱 𝗠𝗜𝗡𝗨𝗧𝗘𝗦 - 𝟱𝟬𝟬 𝗥𝗦  💦
🍒𝟭𝟬 𝗠𝗜𝗡𝗨𝗧𝗘𝗦 - 𝟴𝟬𝟬 𝗥𝗦 💦

       🌟 𝗦𝗘𝗫 𝗖𝗛𝗔𝗧 👄

🍒𝟱 𝗠𝗜𝗡𝗨𝗧𝗘𝗦 - 𝟮𝟬𝟬 𝗥𝗦 💦
🍒𝟭𝟬 𝗠𝗜𝗡𝗨𝗧𝗘𝗦 - 𝟯𝟱𝟬 𝗥𝗦 💦

       🎀 𝗦𝗣𝗘𝗖𝗜𝗔𝗟 𝗦𝗛𝗢𝗪 💘

🍒 𝗦𝗔𝗥𝗘𝗘 𝗦𝗛𝗢𝗪 - 𝟭𝟮𝟬𝟬 𝗥𝗦 💦
🍒 𝗦𝗤𝗨𝗜𝗥𝗧 𝗦𝗛𝗢𝗪 - 𝟭𝟭𝟬𝟬 𝗥𝗦 💦

💟𝗗𝗘𝗠𝗢 - 𝟭𝟬𝟬 𝗥𝗦💟
""")
        
@client.on(events.NewMessage(outgoing=True, pattern=r"\.spam"))
async def spam(event):
    args = event.raw_text.split(maxsplit=2)
    count = int(args[1])
    text = args[2]

    await event.delete()
    for _ in range(count):
        await client.send_message(event.chat_id, text)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.boost"))
async def boost_msg(event):
    await event.edit("𝘽𝙊𝙊𝙎𝙏 𝙏𝙃𝙄𝙎 𝘾𝙃𝘼𝙉𝙉𝙀𝙇 𝙂𝙍𝙊𝙐𝙋 t.me/wife_swapping_gf?boost ❤️")

#@client.on(events.NewMessage(outgoing=True, pattern=r"\.alive"))
#async def alive_msg(event):
 #   await event.edit("I'm alive my queen.. ❤️")

start_time = time.time()

@client.on(events.NewMessage(outgoing=True, pattern=r"\.alive"))
async def alive(event):
    uptime = int(time.time() - start_time)
    await event.edit(f"⚡ 𝙕𝙄𝙉𝘿𝘼 𝙃𝙐...\nUptime: {uptime} sec")

@client.on(events.NewMessage(outgoing=True, pattern=r"\.love"))
async def heart(event):
    frames = [
        "❤️",
        "🧡",
        "💛",
        "💚",
        "💙",
        "💜",
        "❤️"
    ]

    for frame in frames:
        await event.edit(frame)
        await asyncio.sleep(0.4)

@client.on(events.NewMessage(outgoing=True, pattern=r"\.pay"))
async def send_qr(event):
    await client.send_file(
        event.chat_id,
        "qr.jpg",
        caption="𝙎𝘾𝘼𝙉 𝘼𝙉𝘿 𝙋𝘼𝙔 𝘽𝘼𝘽𝙀 💋"
    )
    await event.delete()

@client.on(events.NewMessage(outgoing=True, pattern=r"\.opay"))
async def send_qr(event):
    await client.send_file(
        event.chat_id,
        "oqr.jpg",
        caption="𝙎𝘾𝘼𝙉 𝘼𝙉𝘿 𝙋𝘼𝙔 𝘽𝘼𝘽𝙀 💋"
    )
    await event.delete()
    
async def main():
    await client.start()
    print("Userbot running...")
    await client.run_until_disconnected()

keep_alive()
with client:
    client.loop.run_until_complete(main())
