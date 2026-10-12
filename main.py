
import os
import asyncio
import yt_dlp

from pyrogram import Client, filters, idle
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream, AudioQuality

API_ID = int(os.environ["35663519"])
API_HASH = os.environ["ac3102427c7679d55eef0a9ac4e5a562"]
BOT_TOKEN = os.environ["8807839828:AAER8fc2m_eWxWcJzyCJa8yvOHlbTmWOO4Y"]
SESSION_STRING = os.environ["BQIgLp8Akxh3a5p6rNCG4JWcVE8b6MC5r98zP1e-5dOk4GiR_8POD3HNlW4_8u6GVu7TRVc6LGG6EpvQj4Tq32_UTBELqkejDQdc_Z4QerPAAA3Rzw9L3hROVHc4ABD-SSzOKQ9zAuaqJGUF6sRZTT-8e64ew1dAd5oud_2lwpZEOnwX2RNFWAdkM7KP8EAuw8yMy-_e0DoSgQAz3Nb71JpGOi7zJk8uUhS7A-WJn_j8bHuqIYK0Po7Ci1wjB25Q5bos1526a0AG69PRf5iADq1vCNfkpvAU06koDxiUh7UlfkpQE0N71krR5I5mZ3YPwDmnGu8b_47h3EzP4pU4n6Yc9QcezwAAAAIIYRa1AA"]

bot = Client(
    "music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

user = Client(
    "music_user",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

calls = PyTgCalls(user)


def get_audio(query):
    if not query.startswith(("http://", "https://")):
        query = "ytsearch1:" + query

    options = {
        "format": "bestaudio/best",
        "quiet": True,
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(query, download=False)

        if "entries" in info:
            info = next(
                (item for item in info["entries"] if item),
                None
            )

        if not info:
            raise ValueError("موزیک پیدا نشد.")

        return info["url"], info.get("title", "موزیک")


@bot.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text(
        "سلام! برای پخش موزیک از دستور زیر استفاده کن:\n"
        "/play نام موزیک"
    )


@bot.on_message(filters.command("play") & filters.group)
async def play(_, message):
    if len(message.command) < 2:
        await message.reply_text(
            "مثال:\n/play Arash Broken Angel"
        )
        return

    query = " ".join(message.command[1:])

    status = await message.reply_text(
        "در حال پیدا کردن موزیک..."
    )

    try:
        audio_url, title = await asyncio.to_thread(
            get_audio, query
        )

        await calls.play(
            message.chat.id,
            MediaStream(audio_url, AudioQuality.HIGH)
        )

        await status.edit_text(
            f"در حال پخش موزیک:\n{title}"
        )

    except Exception as error:
        print("PLAY ERROR:", repr(error))
        await status.edit_text(
            "پخش موزیک موفق نشد. گزارش خطا را در Render بررسی کن."
        )


print("Music bot is starting...")

bot.start()
calls.start()

print("Music bot started successfully!")

idle()

calls.stop()
bot.stop()
