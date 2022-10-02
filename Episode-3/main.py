## Imports
import nextcord
import dotenv
import aiosqlite
import datetime
from os import environ as env
from cogs.button import Button
from cogs.test_database import database_commands
cogs = [database_commands, Button]

## Load .env
dotenv.load_dotenv()

## Functions
def get_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

## Create client

class Client(nextcord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f"[{get_time()}] Logged in as {self.user}")

        # Create database
        self.db = await aiosqlite.connect("database.db")

        # Create tables
        async with self.db.cursor() as cursor:
            
            await cursor.execute("CREATE TABLE IF NOT EXISTS test (value TEXT)")
            print(f"[{get_time()}] Created table 'test'")

            await self.db.commit()

client = Client(intents=nextcord.Intents.default())

## Load Cogs

for cog in cogs:
    client.add_cog(cog(client))

## Commands

@client.slash_command(name="ping", description="Pong!")
async def ping(interaction: nextcord.Interaction):
    await interaction.response.send_message(f"Pong! \nLatency: `{round(client.latency * 1000)}ms`")

@client.slash_command(name="embed", description="Returns an embed")
async def embed(
        interaction: nextcord.Interaction, description: str = nextcord.SlashOption(description="Description of the embed", required=True), 
        title: str = nextcord.SlashOption(description="Title of the embed", required=False)
    ):
    embed = nextcord.Embed(description=description)
    if title:
        embed.title = title

    await interaction.response.send_message(embed=embed)


## Run
client.run(env["TOKEN"])