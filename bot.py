from multiprocessing import connection
import discord
import os
import dotenv
import json
import random
import psycopg2

MATHS_SERVER_ID = 992049801216655370
server_name = {792095347819806741: "bot test server", 1018871773040758844: "Maths Part IA", MATHS_SERVER_ID: "Maths Part III"}
veri_role_name = {792095347819806741: "student", MATHS_SERVER_ID: "student"}
INT64_MAX = 18446744073709551616 # 2^64


# set correct working directory
os.chdir(os.path.dirname(__file__))

# get secrets from .env file
dotenv.load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DRA_PASS = os.getenv('DRA_PASS')

DB_CONN = {'database':'dra', 'user':'dra', 'password':DRA_PASS, 'host':'10.100.64.89', 'port':'5432'}

class MyBot(discord.Client):
    async def verify(self, userid):
        user = self.get_user(userid)
        if user:
            try:
                await user.send("Thank you for verifying!")
            except Exception as e:
                print(e)

            for guild in self.guilds:
                rolename = veri_role_name.get(guild.id, "verified")
                veri_role = discord.utils.get(guild.roles,name=rolename)
                if veri_role: # skip if role not found
                    member = guild.get_member(userid)
                    if member: # skip if not in server
                        try:
                            await member.add_roles(veri_role, reason = "Auto-verified")
                            print("Verified userid: " + str(userid) + " for guild: " + server_name[guild.id])
                        except Exception as e:
                            print("Failed to add role " + rolename + " for guild " + str(guild))
                            print(e)

                        # TEMPORARY
                        if guild.id == MATHS_SERVER_ID:
                            try:
                                await member.send("Head to <#992049801388621843> to get access to channels for your courses!")
                            except Exception as e:
                                print(e)
                else:
                    print("Role " + rolename + " not found for server " + str(guild) + " id " + str(guild.id))

    async def unverify(self, userid):
        user = self.get_user(userid)
        if user:
            for guild in self.guilds:
                rolename = veri_role_name.get(guild.id, "verified")
                veri_role = discord.utils.get(guild.roles,name=rolename)
                if veri_role: # skip if role not found
                    member = guild.get_member(userid)
                    if member: # skip if not in server
                        try:
                            await member.remove_roles(veri_role, reason = "Auto-unverified")
                            print("Unverified userid: " + str(userid) + " for guild: " + server_name[guild.id])
                        except Exception as e:
                            print("Failed to remove role " + rolename + " for guild " + str(guild))
                            print(e)
                else:
                    print("Role " + rolename + " not found for server " + str(guild) + " id " + str(guild.id))

    async def on_ping(self, db_conn, id=None):
        db_cursor = db_conn.cursor()
        if id == None:
            # update all unverified users
            db_cursor.execute("SELECT userid FROM partIII.members;")
            ids = [entry[0] for entry in db_cursor.fetchall()]
            print("Updating " + str(len(ids)) + " verified users")
            for id in ids:
                print(id)
                if id.isnumeric():
                    # update individual user
                    await self.on_ping(db_conn, id)
        else:
            id = str(id)
            if id.isnumeric():
                db_cursor.execute("SELECT verified, manualverif FROM partIII.members WHERE userid='"+id+"';")
                data = db_cursor.fetchone() # assume no duplicate entries
                if data[0] or data[1]:
                    await self.verify(int(id))
                else:
                    print("Fake verification signal for userid: " + id)
                    await self.unverify(int(id))
            else:
                print("Invalid verification signal for userid: " + id)
    
    async def update(self, user, join=True):
        db_conn = psycopg2.connect(**DB_CONN)
        print("Connected to database")

        try:
            db_cursor = db_conn.cursor()
            
            id = user.id
            db_cursor.execute("SELECT verified, manualverif FROM partIII.members WHERE userid='"+str(id)+"';")
            data = db_cursor.fetchone()
            if data == None: # new user
                salt = random.randint(0, INT64_MAX - 1)
                salted_id = str((id + salt) % INT64_MAX)
                db_cursor.execute("INSERT INTO partIII.members (userid, verifyd) VALUES ('"+str(id)+"', '"+salted_id+"');")
                db_conn.commit()
                print(str(id) + " joined! New user. Salt: " + str(salt) + "; sent to " + salted_id)
            else:
                if data[0] or data[1]: # already verified
                    print(str(id) + " joined! Already verified")
                    await client.verify(id)
                    if not join:
                        await user.send("You are already verified")
                    return # don't send veri link
                else: # already unverified
                    db_cursor.execute("SELECT verifyd FROM partIII.members WHERE userid='"+str(id)+"';")
                    salted_id = db_cursor.fetchone()[0]
                    print(str(id) + " joined! Already unverified; sent to " + salted_id)

            # DM verification link
            if join:
                await user.send(
                    "Welcome to this Raven-protected server! Please verify yourself at https://dra.soc.srcf.net/partIIIverify/?id=" + salted_id)
            else:
                await user.send(
                    "Please verify yourself at https://dra.soc.srcf.net/partIIIverify/?id=" + salted_id)
        finally:
            db_conn.close()

# allows bot to listen for necessary events
intents = discord.Intents.default()
intents.members = True
intents.messages = True
client = MyBot(intents = intents)

@client.event
async def on_ready():
    print("Discord bot connected")
    await client.change_presence(activity = discord.Game(name="Online")) # online indicator

@client.event
async def on_member_join(member):
    await client.update(member)
    # TODO: restore roles from DB

@client.event
async def on_member_remove(member):
    role_data = [role.name for role in member.roles]
    data_json = json.dumps((role_data, member.guild.id, member.id))
    print(str(member.id) + " left!")
    print(member.guild.id)
    print("data: " + data_json)
    # TODO: save roles to DB

@client.event
async def on_message(message):
    author = message.author
    if author == client.user: # own message
        return
    if not message.guild: # DM
        await message.channel.send("Checking your status...")
        await client.update(author, join=False)

def run_bot():
    client.run(TOKEN)