import time
from config import *
from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types import GroupCallConfig
from motor.motor_asyncio import AsyncIOMotorClient
from .logging import LOGGER


# Bot Client
bot = Client(
    name="Bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN, 
)

# Assistant Client
app = Client(
    name="Assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=str(STRING_SESSION),
)

# Py-TgCalls Client
call = PyTgCalls(app)
call_config = GroupCallConfig(auto_start=False)

# Mongo db Database
mongo_async_cli = AsyncIOMotorClient(MONGO_DB_URL)
mongodb = mongo_async_cli.adityaxdb

# store start time
__start_time__ = time.time()
