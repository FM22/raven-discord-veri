import bot
import server
import threading
import asyncio

threading.Thread(target = server.run_server, args = ()).start()
bot.run_bot()