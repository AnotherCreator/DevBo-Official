# ---       IMPORTS             ---#
import asyncpg
import discord
import os
import psycopg2
from discord.ext import commands, tasks
from dotenvy import load_env, read_file
from itertools import cycle

# ---     BOT INITIALIZATION    --- #

bot = commands.Bot(command_prefix=';')
bot.remove_command('help')

# ---       ENV VARIABLES       --- #

# Bot / Bot Owner related
load_env(read_file('.env'))
SECRET_KEY = os.environ.get('SECRET_KEY')
OWNER_ID = os.environ.get('OWNER_ID')

# ---       DATABASE STUFF      --- #
# PostgreSQL related
CURR_ENV = 'dev'

# Local Database
if CURR_ENV == 'dev':
    DB_DEV_PW = os.environ.get('DB_DEV_PW')

    async def create_db_pool():
        bot.pg_con = await asyncpg.create_pool(database='PyCharmPyBoDB', user='postgres', password=DB_DEV_PW)
# Heroku Database
elif CURR_ENV == 'prod':
    PG_PW = os.environ.get('PG_PW')
    DB_URL = os.environ.get('DB_URL')

    async def heroku_db_pool():
        conn = psycopg2.connect(DB_URL, sslmode='require')
        bot.cur = conn.cursor()

# ---     GLOBAL VARIABLES      --- #

status = cycle(['For more info | ;help', 'Under development! | ;help'])


# ---       BACKGROUND STUFF    --- #

@tasks.loop(seconds=30)
async def change_status():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(next(status)))


# ---       MAIN LINE           --- #

@bot.event
async def on_ready():
    change_status.start()
    print(f'{bot.user.name} is ready!')


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


# ---       LOAD MODULES        --- #

if CURR_ENV == 'dev':
    for filename in os.listdir('./modules'):
        if filename.endswith('.py') and not filename.startswith('-'):
            bot.load_extension(f'modules.{filename[:-3]}')
elif CURR_ENV == 'prod':
    for filename in os.listdir('./modules'):
        if filename.endswith('.py') and not filename.startswith('_'):
            bot.load_extension(f'modules.{filename[:-3]}')


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
if CURR_ENV == 'dev':
    bot.loop.run_until_complete(create_db_pool())
elif CURR_ENV == 'prod':
    bot.loop.run_until_complete(heroku_db_pool())
bot.run(SECRET_KEY)
