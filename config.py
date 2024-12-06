import re
import sys
from os import getenv
from dotenv import load_dotenv

load_dotenv()
API_ID = int(getenv("API_ID", "25742938"))
API_HASH = getenv("API_HASH", "b35b715fe8dc0a58e8048988286fc5b6")
BOT_TOKEN = getenv("BOT_TOKEN", "7792047714:AAFKFkGWgW6fv47JQ1ddLvIilsa9EzG8pg0")
STRING_SESSION = getenv("STRING_SESSION", "BQGIzloAS8aDcjKd8zRdYkAXdQA1FLXOF1S2cERCELpbw5PKX95SDUH1pc8BqkMSm-KJkp2yAtOgHk4JOfjgiuoDFbAE91UCnkCpfZq9dN7HkxCXTw4gis9hpXuDW5xqSXYdxBiI8UxQEk2X430-CVhPBUshzEP3wJj4fP31gN_ffbPZcJytSoC2e1SS0vBHWkUUJITqtLYpObavXaEbFPK0e7o6OtpKnfCzlH4q19K0xY3UqJmNIYAXYkNcse1zbPRu-4n0F6Rcfcd8iIxwm7XlUt5Sf84_T4QGYgvGCjFVWO4cHs-zCHhgtJMkYTyWVoOgQyH9vcuGOBaFntjxOrKTScflRwAAAAF5XDOMAA")
MONGO_DB_URL = getenv("MONGO_DB_URL", "mongodb+srv://hnyx:wywyw2@cluster0.9dxlslv.mongodb.net/?retryWrites=true&w=majority")
OWNER_ID = int(getenv("OWNER_ID", "7009601543"))
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", "-1002293505498"))
START_IMAGE_URL = getenv("START_IMAGE_URL", "https://files.catbox.moe/6v7esb.jpg")
