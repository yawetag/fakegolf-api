import discord
import math
import os
import subprocess
import time

from discord.ext import commands, tasks
from discord.ext.commands import Bot

import keys
import fg_discord.fg_check as check

from fg_discord.fg_messages import send_log

##### DISCORD BOT SETUP #######################################################
TOKEN = keys.discord_token
intents = discord.Intents.all()
intents.members = True
intents.message_content = True
activity = discord.Activity(type=discord.ActivityType.playing, name="Fake Golf")
bot = Bot(command_prefix="-", case_insensitive=True, intents=intents, activity=activity)
###############################################################################

##### DISCORD FUNCTIONS #######################################################
@bot.command(
        hidden=True
)
@commands.has_role(keys.admin_role)
async def reload(ctx, extension):
    """Reloads the given bot module"""
    await bot.unload_extension(f"fg_discord.{extension}")
    await bot.load_extension(f"fg_discord.{extension}")
    await ctx.message.add_reaction('👍')

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} in the following servers:")
    for guild in bot.guilds:
        print(f"   {guild.name} (id: {guild.id})")
    print()
    print(f"Loading the following modules:")
    for filename in os.listdir('fg_discord'):
        if filename.endswith('.py'):
            print(f"   fg_discord.{filename[:-3]}")
            await bot.load_extension(f'fg_discord.{filename[:-3]}')
    git_dis1 = subprocess.getoutput("git dis1").replace(" | ","\n")
    git_dis2 = subprocess.getoutput("git dis2")
    await send_log(None, f"# BOT STARTED\n{git_dis1}\n\n**Diff List:**\n```{git_dis2}```")

    check_tournaments.start()

@tasks.loop(seconds=15)
async def check_tournaments():
    curr_time = math.floor(time.time())
    await check.ck_check_tournaments(bot, curr_time)


bot.run(TOKEN)
###############################################################################S