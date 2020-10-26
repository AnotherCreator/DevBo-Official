# ---       IMPORTS          ---#

import discord
import os
from discord.ext import commands
from dotenvy import load_env, read_file

# ---       GLOBAL VARIABLES          ---#

load_env(read_file('.env'))
SECRET_KEY = os.environ.get('SECRET_KEY')
OWNER_ID = os.environ.get('OWNER_ID')

bot = commands.Bot(command_prefix=';')
bot.remove_command('help')

# ---       FUNCTIONS        ---#


def bot_owner_check(ctx):
    if ctx.author.id == int(OWNER_ID):
        return ctx.author.id

# ---       MAIN LINE        ---#


@commands.command()
@commands.check(bot_owner_check)
async def updatelogs(self, message):
    # 'update-notes' channel
    channel = self.bot.get_channel(768626068629880902)
    embed = discord.Embed(
        title=f'{message}',
        description='',
        colour=discord.Colour.blurple()
    )

    await channel.send(embed=embed)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('For more info | ;help'))
    print(f'{bot.user.name} is ready!')


@bot.command()
@commands.check(bot_owner_check)
async def load(ctx, extension):
    bot.load_extension(f'modules.{extension}')


@bot.command()
@commands.check(bot_owner_check)
async def unload(ctx, extension):
    bot.unload_extension(f'modules.{extension}')

for filename in os.listdir('./modules'):
    if filename.endswith('.py'):
        bot.load_extension(f'modules.{filename[:-3]}')


@bot.command()
@commands.check(bot_owner_check)
async def reload(ctx, extension):
    bot.unload_extension(f'modules.{extension}')
    bot.load_extension(f'modules.{extension}')


# ---       END MAIN        ---#
bot.run(SECRET_KEY)
