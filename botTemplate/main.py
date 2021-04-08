import discord
import os
import psycopg2

from discord.ext import commands
from dotenv import load_dotenv
from psycopg2 import Error

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

DATABASE_URL = os.getenv('DATABASE_URL')

# Set command prefix to whatever special character you like
client = commands.Bot(command_prefix="$")

@client.event
async def on_ready():
    print('Bot is ready!')


# Simple bot response to a command 
@client.command(
    # Both of these parameters are what populate the help command which is auto-created for bots
    help="Define help message",
    brief="Provide summary of command"
)
async def hello(ctx):
    await ctx.channel.send("hello")


# Search a database for some name provided and return the result in channel
@client.command(
    help="",
    brief=""
)
async def search(ctx, name):
    try:
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor
        cursor.execute("SELECT * FROM database WHERE name = %s", (name,))   # Note that there must be a trailing comma in parameters so that it is a tuple
        result = cursor.fetchone()
        if result[0] == None:
            await ctx.channel.send("There is no item of that name in the database")
        else:
            await ctx.channel.send(result[0])
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed after item check")

# Run token
client.run(TOKEN)