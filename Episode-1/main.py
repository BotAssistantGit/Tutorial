## Imports
import nextcord
import dotenv
import aiosqlite
import datetime
from os import environ as env

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

client = Client(intents=nextcord.Intents.default())

## Commands

@client.slash_command(name="ping", description="Pong!")
async def ping(interaction: nextcord.Interaction):
    await interaction.response.send_message(f"Pong! \nLatency: `{round(client.latency * 1000)}ms`")

## Run
client.run(env["TOKEN"])