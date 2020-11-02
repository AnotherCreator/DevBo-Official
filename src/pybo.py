# ---       IMPORTS             ---#
import asyncpg
import discord
import os
import psycopg2
from discord.ext import commands, tasks
from dotenvy import load_env, read_file
from itertools import cycle
 

# ---       GLOBAL VARIABLES          ---#
load_env(read_file('.env'))
SECRET_KEY = os.environ.get('SECRET_KEY')
OWNER_ID = os.environ.get('OWNER_ID')
PG_PW = os.environ.get('PG_PW')

bot = commands.Bot(command_prefix=';')
bot.remove_command('help')

status = cycle(['For more info | ;help', 'Under development! | ;help'])


# ---       FUNCTIONS           --- #
def bot_owner_check(ctx):
    if ctx.author.id == int(OWNER_ID):
        return ctx.author.id


async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(
        database='postgres://zypblmyaueyqrh'
        ':1cdb6059ecd29ad868acd11e840125b05f74b56b93508846c330d01352268dfa@'
        ':ec2-34-200-106-49.compute-1.amazonaws.com:5432/d5vv5mj3ftlf9f',
        user='postgres',
        password=PG_PW
    )


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
@commands.check(bot_owner_check)
async def updatelogs(ctx, *, message):
    # 'update-notes' channel
    channel = bot.get_channel(768626068629880902)

    embed = discord.Embed(
        title='',
        description=f'{message}',
        colour=discord.Colour.blurple()
    )
    embed.set_footer(
        text=ctx.message.created_at(),
    )

    await channel.send(embed=embed)


@bot.command()
@commands.check(bot_owner_check)
async def updateissues(ctx, *, message):
    # 'known-issues' channel
    channel = bot.get_channel(772224003833069618)

    embed = discord.Embed(
        title='',
        description=f'{message}',
        colour=discord.Colour.blurple()
    )
    embed.set_footer(
        text=ctx.message.created_at(),
    )
    await channel.send(embed=embed)


# ---       LOAD MODULES        --- #

@bot.command()
@commands.check(bot_owner_check)
async def load(ctx, extension):
    bot.load_extension(f'modules.{extension}')
    print(f'{extension} has been loaded')


@bot.command()
@commands.check(bot_owner_check)
async def unload(ctx, extension):
    bot.unload_extension(f'modules.{extension}')
    print(f'{extension} has been unloaded')

for filename in os.listdir('./modules'):
    if filename.endswith('.py') and not filename.startswith('_'):
        bot.load_extension(f'modules.{filename[:-3]}')


@bot.command()
@commands.check(bot_owner_check)
async def reload(ctx, extension):
    bot.unload_extension(f'modules.{extension}')
    bot.load_extension(f'modules.{extension}')


# ---       END MAIN            ---#
bot.run(SECRET_KEY)
