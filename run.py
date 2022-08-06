import bot
import server
import _thread

_thread.start_new_thread(server.run_server())
_thread.start_new_thread(bot.run_bot())