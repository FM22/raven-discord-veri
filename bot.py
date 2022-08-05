import discord
import os
import dotenv
import asyncio
import math
import pickle

# set correct working directory
os.chdir(os.path.dirname(__file__))

# get secret token from .env file
dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# allows bot to listen for necessary events
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents = intents)

@client.event
async def on_ready():
    print("Connected")
    await client.change_presence(activity = discord.Game(name="hi"))

@client.event
async def on_member_join(member):
    guild = member.guild
    id = member.id
    print(str(id) + "joined!")
    # DM verification link

@client.event
async def on_member_leave(member):
    pass
    # save role data to backend

# need some way to listen for ping back from website

client.run(TOKEN)