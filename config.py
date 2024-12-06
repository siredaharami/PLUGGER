import re
import sys
from os import getenv
from dotenv import load_dotenv

load_dotenv()
API_ID = int(getenv("API_ID", "25742938"))
API_HASH = getenv("API_HASH", "b35b715fe8dc0a58e8048988286fc5b6")
BOT_TOKEN = getenv("BOT_TOKEN", "7656510911:AAHx2GcEV9q_HOQ5NjysO1V2cMdAaVQpz8Y")
STRING_SESSION = getenv("STRING_SESSION", "BQGIzloAOBgXQvRpl8euAjWpsYdQBDNP2eBae110aMP-eUDCfVdETHfFtRrWxPl1NUXnK2oAX7MyfLL1TdbQ35PuJ8CrrbS5xXxeHN4zR6k7W09ZRkdwuF7GETxKK3gAwtaF3qZmop8xmFjMewyuLP36awmqDKtpP-je4jLif4V2Vyqa2P7zEO-MQT1m0eb0qCI6BkC8WJ5_hWJzy9uEGk_fr-dOnMtffcocMpFrAia1aw_j0z2xTglDoIyW1QlNVH1mU89V00OedRS4TSMkC6_621rhsc9HmcTQ4pGz2We56hJ-hvHjOJfoLnpaWBfybeu3BEW74P6Fxwpm90djdbmymwyZTgAAAAF-_9otAA")
MONGO_DB_URL = getenv("MONGO_DB_URL", "mongodb+srv://hnyx:wywyw2@cluster0.9dxlslv.mongodb.net/?retryWrites=true&w=majority")
OWNER_ID = int(getenv("OWNER_ID", "7475631398"))
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", "-1002356967761"))
START_IMAGE_URL = getenv("START_IMAGE_URL", "https://files.catbox.moe/6v7esb.jpg")
