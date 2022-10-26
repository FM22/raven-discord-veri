import discord
import bot
import os
import dotenv
import sys
import psycopg2

# command line argument
if len(sys.argv) > 1:
    uid = sys.argv[1]
else:
    uid = None

# set correct working directory
os.chdir(os.path.dirname(__file__))

# get secrets from .env file
dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DRA_PASS = os.getenv('DRA_PASS')

DB_CONN = {'database':'dra', 'user':'dra', 'password':DRA_PASS, 'host':'10.100.64.89', 'port':'5432'}

intents = discord.Intents.default()
intents.members = True
intents.messages = True
client = bot.MyBot(intents = intents)

@client.event
async def on_ready():
    if uid == None:
        print("Update bot connected for full reload")
    else:
        print("Update bot connected for id " + str(uid))
    # connect to database
    db_conn = psycopg2.connect(**DB_CONN)
    print("Connected to database")
    try:
        await client.on_ping(db_conn, uid)
    finally:
        # close connection
        db_conn.close()

client.run(TOKEN)