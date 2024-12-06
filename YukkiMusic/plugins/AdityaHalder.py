import aiohttp, aiofiles, asyncio, base64, logging, config
import os, platform, random, re, socket
import sys, time, textwrap
from YukkiMusic import bot as bot, app, call, LOGGER
from os import getenv
from io import BytesIO
from time import strftime
from functools import partial
from dotenv import load_dotenv
from datetime import datetime
from typing import Union, List, Pattern
from logging.handlers import RotatingFileHandler

from PIL import Image, ImageDraw, ImageFont



from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_async_

from pyrogram import Client, filters as pyrofl
from pytgcalls import PyTgCalls, filters as pytgfl


from pyrogram import idle, __version__ as pyro_version
from pytgcalls.__version__ import __version__ as pytgcalls_version

from ntgcalls import TelegramServerError
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import (
    ChatAdminRequired,
    FloodWait,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pytgcalls.exceptions import NoActiveGroupCall
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls.types import ChatUpdate, Update, GroupCallConfig
from pytgcalls.types import Call, MediaStream, AudioQuality, VideoQuality
import os
import re
import textwrap

import aiofiles
import aiohttp
from PIL import (Image, ImageDraw, ImageEnhance, ImageFilter,
                 ImageFont, ImageOps)
from youtubesearchpython.__future__ import VideosSearch

from config import START_IMAGE_URL


from PIL import Image, ImageDraw, ImageEnhance
from PIL import ImageFilter, ImageFont, ImageOps
from youtubesearchpython.__future__ import VideosSearch




# config variables
if os.path.exists("Config.env"):
    load_dotenv("Config.env")

API_ID = int(getenv("API_ID", 0))
API_HASH = getenv("API_HASH", None)
BOT_TOKEN = getenv("BOT_TOKEN", None)
STRING_SESSION = getenv("STRING_SESSION", None)
MONGO_DB_URL = getenv("MONGO_DB_URL", None)
OWNER_ID = int(getenv("OWNER_ID", 0))
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", 0))
START_IMAGE_URL = getenv("START_IMAGE_URL", None)


# Memory Database

ACTIVE_AUDIO_CHATS = []
ACTIVE_VIDEO_CHATS = []
ACTIVE_MEDIA_CHATS = []

QUEUE = {}


# Command & Callback Handlers


def cdx(commands: Union[str, List[str]]):
    return pyrofl.command(commands, ["/", "!", "."])


def cdz(commands: Union[str, List[str]]):
    return pyrofl.command(commands, ["", "/", "!", "."])


def rgx(pattern: Union[str, Pattern]):
    return pyrofl.regex(pattern)


bot_owner_only = pyrofl.user(OWNER_ID)



call_config = GroupCallConfig(auto_start=False)

mongo_async_cli = _mongo_async_(MONGO_DB_URL)
mongodb = mongo_async_cli.adityaxdb

# store start time
__start_time__ = time.time()


# start and run










# Some Required Functions ...!!


def _netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(4096).decode("utf-8").strip("\n\x00")
        if not data:
            break
        return data
    s.close()


async def paste_queue(content):
    loop = asyncio.get_running_loop()
    link = await loop.run_in_executor(None, partial(_netcat, "ezup.dev", 9999, content))
    return link



def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time





# Mongo Database Functions

chatsdb = mongodb.chatsdb
usersdb = mongodb.usersdb




# Served Chats

async def is_served_chat(chat_id: int) -> bool:
    chat = await chatsdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True


async def get_served_chats() -> list:
    chats_list = []
    async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list


async def add_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if is_served:
        return
    return await chatsdb.insert_one({"chat_id": chat_id})



# Served Users

async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True


async def get_served_users() -> list:
    users_list = []
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list


async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": user_id})













# Callback & Message Queries


@bot.on_message(cdx(["start", "help"]) & pyrofl.private)
async def start_message_private(client, message):
    user_id = message.from_user.id
    mention = message.from_user.mention
    await add_served_user(user_id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:5] == "verify":
            pass
            
    else:
        caption = f"""**➻ Hello, {mention}

🥀 I am An ≽ Advanced ≽ High Quality
Bot, I Can Stream 🌿 Audio & Video In
Your ♚ Channel And Group.

🐬 Must Click ❥ Open Command List
Button ⋟ To Get More Info's 🦋 About
My All Commands.

💐 Feel Free ≽ To Use Me › And Share
With Your ☛ Other Friends.**"""
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="🥀 Add Me In Your Chat ✨",
                        url=f"https://t.me/{bot.me.username}?startgroup=true",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🌺 Open Command List 🌷",
                        callback_data="open_command_list",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="💀 Close Menu",
                        callback_data="force_close",
                    )
                ],
            ]
        )
        if START_IMAGE_URL:
            try:
                return await message.reply_photo(
                    photo=START_IMAGE_URL, caption=caption, reply_markup=buttons
                )
            except Exception as e:
                LOGGER.info(f"🚫 Start Image Error: {e}")
                try:
                    return await message.reply_text(text=caption, reply_markup=buttons)
                except Exception as e:
                    LOGGER.info(f"🚫 Start Error: {e}")
                    return
        else:
            try:
                return await message.reply_text(text=caption, reply_markup=buttons)
            except Exception as e:
                LOGGER.info(f"🚫 Start Error: {e}")
                return




@bot.on_callback_query(rgx("open_command_list"))
async def open_command_list_alert(client, query):
    caption = """**🥀 All Members Can Use:**
/play - Stream Only Audio On VC.
/vplay - Stream Audio With Video.

**👾 Only For Chat Admins:**
/pause - Pause Running Stream.
/resume - Resume Paused Stream.
/skip - Skip Current Stream To Next.
/end - Stop Current Running Stream.

**Note:** All Commands Will Work
Only in Channels/Groups."""
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🔙 Back",
                    callback_data="back_to_home",
                )
            ],
        ]
    )
    try:
        return await query.edit_message_text(text=caption, reply_markup=buttons)
    except Exception as e:
        LOGGER.info(f"🚫 Cmd Menu Error: {e}")
        return


@bot.on_callback_query(rgx("back_to_home"))
async def back_to_home_menu(client, query):
    mention = query.from_user.mention
    caption = f"""**➻ Hello, {mention}

🥀 I am An ≽ Advanced ≽ High Quality
Bot, I Can Stream 🌿 Audio & Video In
Your ♚ Channel And Group.

🐬 Must Click ❥ Open Command List
Button ⋟ To Get More Info's 🦋 About
My All Commands.

💐 Feel Free ≽ To Use Me › And Share
With Your ☛ Other Friends.**"""
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🥀 Add Me In Your Chat ✨",
                    url=f"https://t.me/{bot.me.username}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌺 Open Command List 🌷",
                    callback_data="open_command_list",
                )
            ],
        ]
    )
    try:
        return await query.edit_message_text(text=caption, reply_markup=buttons)
    except Exception as e:
        LOGGER.info(f"🚫 Back Menu Error: {e}")
        return


@bot.on_callback_query(rgx("force_close"))
async def delete_cb_query(client, query):
    try:
        return await query.message.delete()
    except Exception:
        return


# Thumbnail Generator Area




def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage


async def gen_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Mins"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(
                        f"cache/thumb{videoid}.png", mode="wb"
                    )
                    await f.write(await resp.read())
                    await f.close()

        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(30))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)
        Xcenter = youtube.width / 2
        Ycenter = youtube.height / 2
        x1 = Xcenter - 250
        y1 = Ycenter - 250
        x2 = Xcenter + 250
        y2 = Ycenter + 250
        logo = youtube.crop((x1, y1, x2, y2))
        logo.thumbnail((520, 520), Image.LANCZOS)
        logo = ImageOps.expand(logo, border=15, fill="white")
        background.paste(logo, (50, 100))
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype("YukkiMusic/assets/font2.ttf", 40)
        font2 = ImageFont.truetype("YukkiMusic/assets/font2.ttf", 70)
        arial = ImageFont.truetype("YukkiMusic/assets/font2.ttf", 30)
        name_font = ImageFont.truetype("YukkiMusic/assets/font2.ttf", 30)
        para = textwrap.wrap(title, width=32)
        j = 0
        draw.text(
            (5, 5), f"nothing", fill="white", font=name_font
        )
        draw.text(
            (600, 150),
            "NOW PLAYING",
            fill="white",
            stroke_width=2,
            stroke_fill="white",
            font=font2,
        )
        for line in para:
            if j == 1:
                j += 1
                draw.text(
                    (600, 340),
                    f"{line}",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="white",
                    font=font,
                )
            if j == 0:
                j += 1
                draw.text(
                    (600, 280),
                    f"{line}",
                    fill="white",
                    stroke_width=1,
                    stroke_fill="white",
                    font=font,
                )

        draw.text(
            (600, 450),
            f"Views : {views[:23]}",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (600, 500),
            f"Duration : {duration[:23]} Mins",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (600, 550),
            f"Channel : {channel}",
            (255, 255, 255),
            font=arial,
        )
        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
        background.save(f"cache/{videoid}.png")
        return f"cache/{videoid}.png"
    except Exception:
        return START_IMAGE_URL
        

    

# Some Functions For VC Player


async def add_active_media_chat(
    chat_id, stream_type
):
    if stream_type == "Audio":
        if chat_id in ACTIVE_VIDEO_CHATS:
            ACTIVE_VIDEO_CHATS.remove(chat_id)
        if chat_id not in ACTIVE_AUDIO_CHATS:
            ACTIVE_AUDIO_CHATS.append(chat_id)
    elif stream_type == "Video":
        if chat_id in ACTIVE_AUDIO_CHATS:
            ACTIVE_AUDIO_CHATS.remove(chat_id)
        if chat_id not in ACTIVE_VIDEO_CHATS:
            ACTIVE_VIDEO_CHATS.append(chat_id)
    if chat_id not in ACTIVE_MEDIA_CHATS:
        ACTIVE_MEDIA_CHATS.append(chat_id)


async def remove_active_media_chat(chat_id):
    if chat_id in ACTIVE_AUDIO_CHATS:
        ACTIVE_AUDIO_CHATS.remove(chat_id)
    if chat_id in ACTIVE_VIDEO_CHATS:
        ACTIVE_VIDEO_CHATS.remove(chat_id)
    if chat_id in ACTIVE_MEDIA_CHATS:
        ACTIVE_MEDIA_CHATS.remove(chat_id)


# VC Player Queue

def create_thumbnail(image_path, save_path, size=(200, 200)):
    image = Image.open(image_path)
    image.thumbnail(size)
    image.save(save_path)



async def add_to_queue(
    chat_id,
    user,
    title,
    duration,
    stream_file,
    stream_type,
    thumbnail,
):
    put = {
        "chat_id": chat_id,
        "user": user,
        "title": title,
        "duration": duration,
        "stream_file": stream_file,
        "stream_type": stream_type,
        "thumbnail": thumbnail,
    }
    check = QUEUE.get(chat_id)
    if check:
        QUEUE[chat_id].append(put)
    else:
        QUEUE[chat_id] = []
        QUEUE[chat_id].append(put)

    return len(QUEUE[chat_id]) - 1


async def clear_queue(chat_id):
    check = QUEUE.get(chat_id)
    if check:
        QUEUE.pop(chat_id)


# Log All Streams


async def stream_logger(
    chat_id, user, title, duration, stream_type, thumbnail, position=None
):
    if LOG_GROUP_ID != 0:
        if chat_id != LOG_GROUP_ID:
            chat = await bot.get_chat(chat_id)
            chat_name = chat.title
            if chat.username:
                chat_link = f"@{chat.username}"
            else:
                chat_link = "Private Chat"
            try:
                if user.username:
                    requested_by = f"@{user.username}"
                else:
                    requested_by = user.mention
            except Exception:
                requested_by = user.title
            if position:
                caption = f"""**✅ Added To Queue At :** `#{position}`

**🥀 Title:** {title}
**🐬 Duration:** {duration}
**🦋 Stream Type:** {stream_type}
**🌺 Chat Name:** {chat_name}
**🌼 Chat Link:** {chat_link}
**👾 Requested By:** {requested_by}"""
            else:
                caption = f"""**✅ Started Streaming On VC.**

**🥀 Title:** {title}
**🐬 Duration:** {duration}
**🦋 Stream Type:** {stream_type}
**🌺 Chat Name:** {chat_name}
**🌼 Chat Link:** {chat_link}
**👾 Requested By:** {requested_by}"""
            try:
                await bot.send_photo(LOG_GROUP_ID, photo=thumbnail, caption=caption)
            except Exception:
                pass


# Change stream & Close Stream


async def change_stream(chat_id):
    queued = QUEUE.get(chat_id)
    if queued:
        queued.pop(0)
    if not queued:
        await bot.send_message(chat_id, "**❎ Queue is Empty, So Left\nFrom VC❗...**")
        return await close_stream(chat_id)

    title = queued[0].get("title")
    duration = queued[0].get("duration")
    stream_file = queued[0].get("stream_file")
    stream_type = queued[0].get("stream_type")
    thumbnail = queued[0].get("thumbnail")
    try:
        requested_by = queued[0].get("user").mention
    except Exception:
        if queued[0].get("user").username:
            requested_by = (
                "["
                + queued[0].get("user").title
                + "](https://t.me/"
                + queued[0].get("user").username
                + ")"
            )
        else:
            requested_by = queued[0].get("user").title

    if stream_type == "Audio":
        stream_media = MediaStream(
            media_path=stream_file,
            video_flags=MediaStream.Flags.IGNORE,
            audio_parameters=AudioQuality.STUDIO,
            ytdlp_parameters="--cookies cookies.txt",
        )
    elif stream_type == "Video":
        stream_media = MediaStream(
            media_path=stream_file,
            audio_parameters=AudioQuality.STUDIO,
            video_parameters=VideoQuality.HD_720p,
            ytdlp_parameters="--cookies cookies.txt",
        )

    await call.play(chat_id, stream_media, config=call_config)
    await add_active_media_chat(chat_id, stream_type)
    caption = f"""**✅ Started Streaming On VC.**

**🥀 Title:** {title}
**🐬 Duration:** {duration}
**🦋 Stream Type:** {stream_type}
**👾 Requested By:** {requested_by}"""
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🗑️ Close",
                    callback_data="force_close",
                )
            ],
        ]
    )
    return await bot.send_photo(chat_id, thumbnail, caption, reply_markup=buttons)


async def close_stream(chat_id):
    try:
        await call.leave_call(chat_id)
    except Exception:
        pass
    await clear_queue(chat_id)
    await remove_active_media_chat(chat_id)


# Get Call Status


async def get_call_status(chat_id):
    calls = await call.calls
    chat_call = calls.get(chat_id)
    if chat_call:
        status = chat_call.capture
        if status == Call.Status.IDLE:
            call_status = "IDLE"
        elif status == Call.Status.ACTIVE:
            call_status = "PLAYING"

        elif status == Call.Status.PAUSED:
            call_status = "PAUSED"
    else:
        call_status = "NOTHING"

    return call_status


@bot.on_message(cdz(["play", "vplay"]) & ~pyrofl.private)
async def stream_audio_or_video(client, message):
    try:
        await message.delete()
    except Exception:
        pass
    chat_id = message.chat.id
    await add_served_chat(chat_id)
    user = message.from_user if message.from_user else message.sender_chat
    replied = message.reply_to_message
    audio = (replied.audio or replied.voice) if replied else None
    video = (replied.video or replied.document) if replied else None
    stickers = [
        "🌹",
        "🌺",
        "🎉",
        "🎃",
        "💥",
        "🦋",
        "🕊️",
        "❤️",
        "💖",
        "💝",
        "💗",
        "💓",
        "💘",
        "💞",
    ]
    aux = await message.reply_text(random.choice(stickers))
    if audio:
        title = "Unsupported Title"
        duration = "Unknown"
        try:
            stream_file = await replied.download()
        except Exception:
            return
        result_x = None
        stream_type = "Audio"

    elif video:
        title = "Unsupported Title"
        duration = "Unknown"
        try:
            stream_file = await replied.download()
        except Exception:
            return
        result_x = None
        stream_type = "Video"

    else:
        if len(message.command) < 2:
            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🗑️ Close",
                            callback_data="force_close",
                        )
                    ],
                ]
            )
            return await aux.edit_text(
                "**🥀 Give Me Some Query To\nPlay Audio Or Video❗...\n\nℹ️ Examples:\n≽ Audio: `/play satisfya`\n≽ Video: `/vplay satisfya`**",
                reply_markup=buttons,
            )
        query = message.text.split(None, 1)[1]
        if "https://" in query:
            base = r"(?:https?:)?(?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube(?:\-nocookie)?\.(?:[A-Za-z]{2,4}|[A-Za-z]{2,3}\.[A-Za-z]{2})\/)?(?:shorts\/|live\/)?(?:watch|embed\/|vi?\/)*(?:\?[\w=&]*vi?=)?([^#&\?\/]{11}).*$"
            resu = re.findall(base, query)
            vidid = resu[0] if resu[0] else None
        else:
            vidid = None
        url = f"https://www.youtube.com/watch?v={vidid}" if vidid else None
        search_query = url if url else query
        results = VideosSearch(search_query, limit=1)
        for result in (await results.next())["result"]:
            vid_id = vidid if vidid else result["id"]
            vid_url = url if url else result["link"]
            try:
                title = "[" + (result["title"][:18]) + "]" + f"({vid_url})"
                title_x = result["title"]
            except Exception:
                title = "Unsupported Title"
                title_x = title
            try:
                durationx = result.get("duration")
                if not durationx:
                    duration = "Live Stream"
                    duration_x = "Live"
                elif len(durationx) == 4 or len(durationx) == 7:
                    duration = f"0{durationx} Mins"
                    duration_x = f"0{durationx}"
                else:
                    duration = f"{durationx} Mins"
                    duration_x = f"{duration}"
            except Exception:
                duration = "Unknown"
                duration_x = "Unknown Mins"
            try:
                views = result["viewCount"]["short"]
            except Exception:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except Exception:
                channel = "Unknown Channel"
        stream_file = url if url else result["link"]
        result_x = {
            "title": title_x,
            "id": vid_id,
            "link": vid_url,
            "duration": duration_x,
            "views": views,
            "channel": channel,
        }
        stream_type = "Audio" if str(message.command[0][0]) != "v" else "Video"

    try:
        requested_by = user.mention
    except Exception:
        if user.username:
            requested_by = "[" + user.title + "](https://t.me/" + user.username + ")"
        else:
            requested_by = user.title
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🗑️ Close",
                    callback_data="force_close",
                )
            ],
        ]
    )
    if stream_type == "Audio":
        stream_media = MediaStream(
            media_path=stream_file,
            video_flags=MediaStream.Flags.IGNORE,
            audio_parameters=AudioQuality.STUDIO,
            ytdlp_parameters="--cookies cookies.txt",
        )
    elif stream_type == "Video":
        stream_media = MediaStream(
            media_path=stream_file,
            audio_parameters=AudioQuality.STUDIO,
            video_parameters=VideoQuality.HD_720p,
            ytdlp_parameters="--cookies cookies.txt",
        )
    call_status = await get_call_status(chat_id)
    try:
        if call_status == "PLAYING" or call_status == "PAUSED":
            try:
                thumbnail = await create_thumbnail(result_x, user.id)
                position = await add_to_queue(
                    chat_id, user, title, duration, stream_file, stream_type, thumbnail
                )
                caption = f"""**✅ Added To Queue At :** `#{position}`

**🥀 Title:** {title}
**🐬 Duration:** {duration}
**🦋 Stream Type:** {stream_type}
**👾 Requested By:** {requested_by}"""
                await bot.send_photo(chat_id, thumbnail, caption, reply_markup=buttons)
                await stream_logger(
                    chat_id, user, title, duration, stream_type, thumbnail, position
                )
            except Exception as e:
                try:
                    return await aux.edit(f"**Queue Error:** `{e}`")
                except Exception:
                    LOGGER.info(f"Queue Error: {e}")
                    return
        elif call_status == "IDLE" or call_status == "NOTHING":
            try:
                await call.play(chat_id, stream_media, config=call_config)
            except NoActiveGroupCall:
                try:
                    assistant = await bot.get_chat_member(chat_id, app.me.id)
                    if (
                        assistant.status == ChatMemberStatus.BANNED
                        or assistant.status == ChatMemberStatus.RESTRICTED
                    ):
                        try:
                            return await aux.edit_text(
                                f"**🤖 At First, Unban [Assistant ID](https://t.me/{app.me.username}) To Start Stream❗**"
                            )
                        except Exception:
                            LOGGER.info(
                                f"🤖 At First, Unban Assistant ID To Start Stream❗**"
                            )
                            return
                except ChatAdminRequired:
                    try:
                        return await aux.edit_text(
                            "**🤖 At First, Promote Me as An Admin❗**"
                        )
                    except Exception:
                        LOGGER.info("**🤖 At First, Promote Me as An Admin❗**")
                        return
                except UserNotParticipant:
                    if message.chat.username:
                        invitelink = message.chat.username
                        try:
                            await app.resolve_peer(invitelink)
                        except Exception:
                            pass
                    else:
                        try:
                            invitelink = await bot.export_chat_invite_link(chat_id)
                        except ChatAdminRequired:
                            return await aux.edit_text(
                                "**🤖 Hey, I need invite user permission to add Assistant ID❗**"
                            )
                        except Exception as e:
                            try:
                                return await aux.edit_text(
                                    f"**🚫 Assistant Error:** `{e}`"
                                )
                            except Exception:
                                pass
                            LOGGER.info(f"🚫 Assistant Error: {e}")
                            return
                    try:
                        await asyncio.sleep(1)
                        await app.join_chat(invitelink)
                    except InviteRequestSent:
                        try:
                            await bot.approve_chat_join_request(chat_id, adi.me.id)
                        except Exception as e:
                            try:
                                return await aux.edit_text(
                                    f"**🚫 Approve Error:** `{e}`"
                                )
                            except Exception:
                                pass
                            LOGGER.info(f"🚫 Approve Error: {e}")
                            return
                    except UserAlreadyParticipant:
                        pass
                    except Exception as e:
                        try:
                            return await aux.edit_text(
                                f"**🚫 Assistant Join Error:** `{e}`"
                            )
                        except Exception:
                            pass
                        LOGGER.info(f"🚫 Assistant Join Error: {e}")
                        return
                try:
                    await call.play(chat_id, stream_media, config=call_config)
                except NoActiveGroupCall:
                    try:
                        return await aux.edit_text(f"**⚠️ No Active VC❗...**")
                    except Exception:
                        LOGGER.info(f"⚠️ No Active VC ({chat_id})❗... ")
                        return
            except TelegramServerError:
                return await aux.edit_text("**⚠️ Telegram Server Issue❗...**")
            try:
                thumbnail = await create_thumbnail(result_x, user.id)
                position = await add_to_queue(
                    chat_id, user, title, duration, stream_file, stream_type, thumbnail
                )
                caption = f"""**✅ Started Streaming On VC.**

**🥀 Title:** {title}
**🐬 Duration:** {duration}
**🦋 Stream Type:** {stream_type}
**👾 Requested By:** {requested_by}"""
                await bot.send_photo(chat_id, thumbnail, caption, reply_markup=buttons)
                await stream_logger(
                    chat_id, user, title, duration, stream_type, thumbnail
                )
            except Exception as e:
                try:
                    return await aux.edit(f"**Send Error:** `{e}`")
                except Exception:
                    LOGGER.info(f"Send Error: {e}")
                    return
        else:
            return
        try:
            await aux.delete()
        except Exception:
            pass
        await add_active_media_chat(chat_id, stream_type)
        return
    except Exception as e:
        try:
            return await aux.edit_text(f"**Stream Error:** `{e}`")
        except Exception:
            LOGGER.info(f"🚫 Stream Error: {e}")
            return


@bot.on_message(cdx(["pause", "vpause"]) & ~pyrofl.private)
async def pause_running_stream_on_vc(client, message):
    chat_id = message.chat.id
    try:
        await message.delete()
    except Exception:
        pass
    try:
        call_status = await get_call_status(chat_id)
        if call_status == "IDLE" or call_status == "NOTHING":
            return await message.reply_text("**❎ Nothing Streaming❗**")

        elif call_status == "PAUSED":
            return await message.reply_text("**🔈 Already Paused❗**")
        elif call_status == "PLAYING":
            await call.pause_stream(chat_id)
            return await message.reply_text("**🔈 Stream Paused❗**")
        else:
            return
    except Exception as e:
        try:
            await bot.send_message(chat_id, f"**🚫 Stream Pause Error:** `{e}`")
        except Exception:
            LOGGER.info(f"🚫 Stream Pause Error: {e}")
            return


@bot.on_message(cdx(["resume", "vresume"]) & ~pyrofl.private)
async def resume_paused_stream_on_vc(client, message):
    chat_id = message.chat.id
    try:
        await message.delete()
    except Exception:
        pass
    try:
        call_status = await get_call_status(chat_id)
        if call_status == "IDLE" or call_status == "NOTHING":
            return await message.reply_text("**❎ Nothing Streaming❗**")

        elif call_status == "PLAYING":
            return await message.reply_text("**🔊 Already Streaming❗**")
        elif call_status == "PAUSED":
            await call.resume_stream(chat_id)
            return await message.reply_text("**🔊 Stream Resumed❗**")
        else:
            return
    except Exception as e:
        try:
            await bot.send_message(chat_id, f"**🚫 Stream Resume Error:** `{e}`")
        except Exception:
            LOGGER.info(f"🚫 Stream Resume Error: {e}")
            return


@bot.on_message(cdx(["skip", "vskip"]) & ~pyrofl.private)
async def skip_and_change_stream(client, message):
    chat_id = message.chat.id
    try:
        await message.delete()
    except Exception:
        pass
    try:
        call_status = await get_call_status(chat_id)
        if call_status == "IDLE" or call_status == "NOTHING":
            return await bot.send_message(chat_id, "**❎ Nothing Streaming❗...**")
        elif call_status == "PLAYING" or call_status == "PAUSED":
            stickers = [
                "🌹",
                "🌺",
                "🎉",
                "🎃",
                "💥",
                "🦋",
                "🕊️",
                "❤️",
                "💖",
                "💝",
                "💗",
                "💓",
                "💘",
                "💞",
            ]
            aux = await message.reply_text(random.choice(stickers))
            await change_stream(chat_id)
            try:
                await aux.delete()
            except Exception:
                pass
    except Exception as e:
        try:
            await bot.send_message(chat_id, f"**🚫 Skip Error:** `{e}`")
        except Exception:
            LOGGER.info(f"🚫 Skip Error: {e}")
            return


@bot.on_message(cdx(["end", "vend"]) & ~pyrofl.private)
async def stop_stream_and_leave_vc(client, message):
    chat_id = message.chat.id
    try:
        await message.delete()
    except Exception:
        pass
    try:
        call_status = await get_call_status(chat_id)
        if call_status == "NOTHING":
            return await message.reply_text("**❎ Nothing Streaming❗**")
        elif call_status == "IDLE":
            return await message.reply_text("**✅ Succesfully Left From VC❗**")
        elif call_status == "PLAYING" or call_status == "PAUSED":
            await close_stream(chat_id)
            return await message.reply_text("**❎ Stopped Stream & Left\nFrom VC❗...**")
        else:
            return
    except Exception as e:
        try:
            await bot.send_message(chat_id, f"**🚫 Stream End Error:** `{e}`")
        except Exception:
            LOGGER.info(f"🚫 Stream End Error: {e}")
            return


@call.on_update(pytgfl.chat_update(ChatUpdate.Status.CLOSED_VOICE_CHAT))
@call.on_update(pytgfl.chat_update(ChatUpdate.Status.KICKED))
@call.on_update(pytgfl.chat_update(ChatUpdate.Status.LEFT_GROUP))
async def stream_services_handler(_, update: Update):
    chat_id = update.chat_id
    return await close_stream(chat_id)


@call.on_update(pytgfl.stream_end())
async def stream_end_handler(_, update: Update):
    chat_id = update.chat_id
    return await change_stream(chat_id)


@bot.on_message(cdx("ping") & ~pyrofl.bot)
async def check_sping(client, message):
    start = datetime.now()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    m = await message.reply_text("**🤖 Ping...!!**")
    await m.edit(f"**🤖 Pinged...!!\nLatency:** `{ms}` ms")


@bot.on_message(cdx(["repo", "repository"]) & ~pyrofl.bot)
async def git_repo_link(client, message):
    if message.sender_chat:
        mention = message.sender_chat.title
    else:
        mention = message.from_user.mention
    if message.chat.type == ChatType.PRIVATE:
        caption = f"""**➻ Hello, {mention}
    
🥀 I am An ≽ Advanced ≽ High Quality
Bot, I Can Stream 🌿 Audio & Video In
Your ♚ Channel And Group.

🐬 Feel Free ≽ To Use Me › And Share
With Your ☛ Other Friends.**"""
    else:
        caption = f"**➻ Hello, {mention}.**"
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🌺 Open Repository Link 🦋",
                    url="https://github.com/AdityaHalder/AdityaPlayer",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🗑️ Close",
                    callback_data="force_close",
                )
            ],
        ]
    )
    try:
        await message.reply_photo(
            photo=START_IMAGE_URL, caption=caption, reply_markup=buttons
        )
    except Exception as e:
        LOGGER.info(f"🚫 Error: {e}")
        return


@bot.on_message(cdx("update") & bot_owner_only)
async def update_repo_latest(client, message):
    response = await message.reply_text("Checking for available updates...")
    try:
        repo = Repo()
    except GitCommandError:
        return await response.edit("Git Command Error")
    except InvalidGitRepositoryError:
        return await response.edit("Invalid Git Repsitory")
    to_exc = f"git fetch origin main &> /dev/null"
    os.system(to_exc)
    await asyncio.sleep(3)
    verification = ""
    REPO_ = repo.remotes.origin.url.split(".git")[0]  # main git repository
    for checks in repo.iter_commits(f"HEAD..origin/aditya"):
        verification = str(checks.count())
    if verification == "":
        return await response.edit("Bot is up-to-date!")
    updates = ""
    ordinal = lambda format: "%d%s" % (
        format,
        "tsnrhtdd"[(format // 10 % 10 != 1) * (format % 10 < 4) * format % 10 :: 4],
    )
    for info in repo.iter_commits(f"HEAD..origin/aditya"):
        updates += f"<b>➣ #{info.count()}: [{info.summary}]({REPO_}/commit/{info}) by -> {info.author}</b>\n\t\t\t\t<b>➥ Commited on:</b> {ordinal(int(datetime.fromtimestamp(info.committed_date).strftime('%d')))} {datetime.fromtimestamp(info.committed_date).strftime('%b')}, {datetime.fromtimestamp(info.committed_date).strftime('%Y')}\n\n"
    _update_response_ = "<b>A new update is available for the Bot!</b>\n\n➣ Pushing Updates Now</code>\n\n**<u>Updates:</u>**\n\n"
    _final_updates_ = _update_response_ + updates
    if len(_final_updates_) > 4096:
        link = await paste_queue(updates)
        url = link + "/index.txt"
        nrs = await response.edit(
            f"<b>A new update is available for the Bot!</b>\n\n➣ Pushing Updates Now</code>\n\n**<u>Updates:</u>**\n\n[Click Here to checkout Updates]({url})"
        )
    else:
        nrs = await response.edit(_final_updates_, disable_web_page_preview=True)
    os.system("git stash &> /dev/null && git pull")
    await response.edit(
        f"{nrs.text}\n\nBot was updated successfully! Now, wait for 1 - 2 mins until the bot reboots!"
    )
    os.system("pip3 install -r requirements.txt --force-reinstall")
    os.system(f"kill -9 {os.getpid()} && python3 -m YukkiMusic")
    sys.exit()
    return


@bot.on_message(cdx(["stats"]) & ~pyrofl.private)
async def check_bot_stats(client, message):
    try:
        await message.delete()
    except:
        pass
    photo = START_IMAGE_URL
    caption = "**⏤͟͞ADITYA PLAYER STATS ༗**"
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🐬 Check Stats",
                    callback_data="check_stats",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🗑️ Close",
                    callback_data="force_close",
                )
            ]
        ]
    )
    return await message.reply_photo(
        photo=photo,
        caption=caption,
        reply_markup=buttons,
    )



@bot.on_callback_query(rgx("check_stats"))
async def check_total_stats(client, query):
    try:
        user_id = query.from_user.id
        runtime = __start_time__
        boot_time = int(time.time() - runtime)
        uptime = get_readable_time((boot_time))
        served_chats = len(await get_served_chats())
        served_users = len(await get_served_users())
        activ_chats = len(ACTIVE_MEDIA_CHATS)
        audio_chats = len(ACTIVE_AUDIO_CHATS)
        video_chats = len(ACTIVE_VIDEO_CHATS)
        
        return await query.answer(
            f"""⏱️ Bot Run Time [Boot]
☛ {uptime}

🔴 Served Chats: {served_chats}
🔵 Served Users: {served_users}

🦋 Total Active Chats [{activ_chats}]
✿⋟ Audio Stream: {audio_chats}
✿⋟ Video Stream: {video_chats}""",
            show_alert=True
        )
    except Exception as e:
        LOGGER.info(f"🚫 Stats Error: {e}")
        pass


@bot.on_message(cdx(["broadcast", "gcast"]) & bot_owner_only)
async def broadcast_message(client, message):
    try:
        await message.delete()
    except:
        pass
    if message.reply_to_message:
        x = message.reply_to_message.id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text("**♻️ Usage**:\n/broadcast [Message] Or [Reply To a Message]")
        query = message.text.split(None, 1)[1]
        if "-pin" in query:
            query = query.replace("-pin", "")
        if "-nobot" in query:
            query = query.replace("-nobot", "")
        if "-pinloud" in query:
            query = query.replace("-pinloud", "")
        if "-user" in query:
            query = query.replace("-user", "")
        if query == "":
            return await message.reply_text("**🥀 Please Give Me Some Text To Broadcast❗...**")
    
    # Bot broadcast inside chats
    if "-nobot" not in message.text:
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = (
                    await bot.forward_messages(i, y, x)
                    if message.reply_to_message
                    else await bot.send_message(i, text=query)
                )
                if "-pin" in message.text:
                    try:
                        await m.pin(disable_notification=True)
                        pin += 1
                    except Exception:
                        continue
                elif "-pinloud" in message.text:
                    try:
                        await m.pin(disable_notification=False)
                        pin += 1
                    except Exception:
                        continue
                sent += 1
            except FloodWait as e:
                flood_time = int(e.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except Exception:
                continue
        try:
            await message.reply_text("**✅ Broadcast Messages In {0}  Chats With {1} Pins From Bot.**".format(sent, pin))
        except:
            pass

    # Bot broadcasting to users
    if "-user" in message.text:
        susr = 0
        served_users = []
        susers = await get_served_users()
        for user in susers:
            served_users.append(int(user["user_id"]))
        for i in served_users:
            try:
                m = (
                    await bot.forward_messages(i, y, x)
                    if message.reply_to_message
                    else await bot.send_message(i, text=query)
                )
                susr += 1
            except FloodWait as e:
                flood_time = int(e.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except Exception:
                pass
        try:
            await message.reply_text("**✅ Broadcast Messages To {0} Users.**".format(susr))
        except:
            pass
