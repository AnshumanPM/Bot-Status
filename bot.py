import asyncio
import datetime
import os
import pytz
from pyrogram import Client
from pyrogram.errors import FloodWait

app = Client(
    name="botstatus",
    api_id=int(os.environ.get("API_ID", "")),
    api_hash=os.environ.get("API_HASH", ""),
    session_string=os.environ.get(
        "SESSION_STRING",
        "",
    ),
)
TIME_ZONE = os.environ.get("TIME_ZONE", "")
BOT_LIST = [
    i.strip()
    for i in os.environ.get(
        "BOT_LIST",
        "",
    ).split(" ")
]
CHANNEL_OR_GROUP_ID = int(os.environ.get("CHANNEL_OR_GROUP_ID", ""))
MESSAGE_ID = int(os.environ.get("MESSAGE_ID", ""))
BOT_ADMIN_IDS = [
    int(i.strip()) for i in os.environ.get("BOT_ADMIN_IDS", "").split(" ")
]


async def main():
    async with app:
        while True:
            print("Checking...")
            edit_text = f"📈 | **Real-Time Bot Status**\n\n"
            for index, bot in enumerate(BOT_LIST, start=1):
                try:
                    snt = await app.send_message(bot, "/start")
                    await asyncio.sleep(10)
                    msg_history = app.get_chat_history(bot, limit=1)
                    async for last_msg in msg_history:
                        last_msg_id = last_msg.id
                    if snt.id == last_msg_id:
                        edit_text += (
                            f"**{index}.** 🤖  @{bot}\n            └ **Offline** ❌\n\n"
                        )
                        for bot_admin_id in BOT_ADMIN_IDS:
                            try:
                                await app.send_message(
                                    int(bot_admin_id),
                                    f"🚨 **Beep! Beep!! @{bot} is down** ❌",
                                )
                            except Exception:
                                pass
                        await app.read_chat_history(bot)
                    else:
                        edit_text += (
                            f"**{index}.** 🤖  @{bot}\n            └ **Online** ✅\n\n"
                        )
                        await app.read_chat_history(bot)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
            time = datetime.datetime.now(pytz.timezone(f"{TIME_ZONE}"))
            last_update = time.strftime(f"%d %b %Y at %I:%M %p")
            edit_text += f"\n**✔️ Last checked on:** {last_update} ({TIME_ZONE})\n\n<i>♻️ Refreshes automatically</i>"
            await app.edit_message_text(int(CHANNEL_OR_GROUP_ID), MESSAGE_ID, edit_text)
            print(f"Last checked on: {last_update}")
            await asyncio.sleep(10800)


app.run(main())
