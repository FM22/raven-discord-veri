import discord
import os
import dotenv
import asyncio
import math
import json
import pickle
import random

server_name = {38539 : "bot test server"}
INT64_MAX = 18446744073709551616 # 2^64

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
    salt = random.randint(0, INT64_MAX - 1)
    salted_id = (id + salt) % INT64_MAX
    print(str(id) + " joined! Salt: " + str(salt) + "; sent to " + str(salted_id))
    await member.send(
        "Welcome to " + server_name.get(guild.id, "unregistered server") + 
        " ! Please verify yourself at https://dra.soc.srcf.net/partIIIverify/?id=" + str (salted_id))
    # DM verification link

@client.event
async def on_member_remove(member):
    role_data = [role.name for role in member.roles]
    data_json = json.dumps((role_data, member.guild.id, member.id))
    print(str(member.id) + " left!")
    print("data: " + data_json)
    # save data to backend

async def on_ping():
    print("ping")
    # update roles using database

client.run(TOKEN)