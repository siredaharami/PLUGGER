import asyncio
from pyrogram import idle
from YukkiMusic import bot, app, call

loop = asyncio.get_event_loop()

async def main():
      await bot.start()  
      await app.start() 
      await call.start()
      await idle() 
    

if __name__ == "__main__":
     print("Bot is starting...")
     loop.run_until_complete(main())
