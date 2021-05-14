# ---       IMPORTS             ---#
import asyncio

import asyncpg
import discord
import os
import psycopg2
from discord.ext import commands, tasks
from dotenvy import load_env, read_file
from itertools import cycle

# ---       ENV VARIABLES       --- #

# Bot / Bot Owner related

load_env(read_file('.env'))
SECRET_KEY = os.environ.get('SECRET_KEY')
OWNER_ID = os.environ.get('OWNER_ID')
BOT_AVATAR = os.environ.get('BOT_AVATAR')
# Database
DB_URL = os.environ.get('HEROKU_DB_URL')
# API
API_KEY = os.environ.get('CMC_API_KEY')

# ---     BOT INITIALIZATION    --- #
bot = commands.Bot(command_prefix=';')
bot.remove_command('help')

for filename in os.listdir('modules'):  # Load modules
    if filename.endswith('.py'):
        bot.load_extension(f'modules.{filename[:-3]}')

# ---       MODULE IMPORTS             --- #
# Module imports cant be at the top because 'pybo.py' has to first load all the modules
from modules.market import update_coins


# ---       DATABASE STUFF      --- #
async def create_db_pool():
    # 'self.bot.pg_con' to connect to db in /module files
    bot.pg_con = await asyncpg.create_pool(database='PyBo_Local', user='postgres', password=DB_DEV_PW)

    con = psycopg2.connect(DB_URL, sslmode='require')
    cur = con.cursor()
# ---       BACKGROUND STUFF    --- #
status = cycle(['For more info | ;help', 'Under development! | ;help'])


@tasks.loop(seconds=30)
async def change_status():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(next(status)))


async def refresh_coins():  # Refreshes every 3 minute(s)
    await bot.wait_until_ready()
    while not bot.is_closed():
        update_coins()
        await asyncio.sleep(180)


# ---       MAIN LINE           --- #
@bot.event
async def on_ready():
    change_status.start()
    print(f'{bot.user.name} is ready!')


@bot.command()
@commands.is_owner()
async def botmessage(ctx, *, message):
    channel = bot.get_channel(666873106857721869)
    await channel.send(message)


@bot.command()
@commands.is_owner()
async def updatelogs(ctx, *, message):
    # 'update-notes' channel
    channel = bot.get_channel(768626068629880902)

    embed = discord.Embed(
        title='',
        description=f'{message}',
        colour=discord.Colour.blurple()
    )
    await channel.send(embed=embed)


@bot.command()
@commands.is_owner()
async def updateissues(ctx, *, message):
    # 'known-issues' channel
    channel = bot.get_channel(772224003833069618)

    embed = discord.Embed(
        title='',
        description=f'{message}',
        colour=discord.Colour.blurple()
    )
    await channel.send(embed=embed)


# ---       MODULE HANDLING        --- #
@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f'modules.{extension}')
    print(f'{extension} has been loaded')


@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f'modules.{extension}')
    print(f'{extension} has been unloaded')


@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    bot.unload_extension(f'modules.{extension}')
    bot.load_extension(f'modules.{extension}')


# ---       END MAIN            ---#
bot.loop.create_task(refresh_coins())
bot.loop.run_until_complete(create_db_pool())
bot.run(SECRET_KEY)
