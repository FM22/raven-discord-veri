import discord
import os
import dotenv
import asyncio
import math
import json
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
    await client.change_presence(activity = discord.Game(name="Online")) # online indicator

@client.event
async def on_member_join(member):
    guild = member.guild
    id = member.id
    print(str(id) + " joined!")
    await member.send("Hi! Your user id is " + str(id))
    # DM verification link

@client.event
async def on_member_remove(member):
    role_data = [role.name for role in member.roles]
    data_json = json.dumps((role_data, member.guild.id, member.id))
    print(str(member.id) + " left!")
    print("data: " + data_json)
    # save data to backend

# need some way to listen for ping back from website

client.run(TOKEN)