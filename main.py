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
    # Show list of connected servers to console.
    print(f"Logged in as {bot.user} in the following servers:")
    for guild in bot.guilds:
        print(f"   {guild.name} (id: {guild.id})")
    print()
    
    # Show list of loaded modules to the console.
    print(f"Loading the following modules:")
    for filename in os.listdir('fg_discord'):
        if filename.endswith('.py'):
            print(f"   fg_discord.{filename[:-3]}")
            await bot.load_extension(f'fg_discord.{filename[:-3]}')
    
    # Get git info
    git_branch_local = subprocess.getoutput("git branch --show-current")
    git_id_local = subprocess.getoutput(f"git rev-parse --short {git_branch_local}")
    git_id_remote = subprocess.getoutput(f"git rev-parse --short origin/{git_branch_local}")
    git_commit_desc = subprocess.getoutput(f"git log -1 --pretty=%B")
    git_diff_list = subprocess.getoutput("git dis2")

    if git_id_local != git_id_remote:
        git_id_msg = "*** DIFFERENT ***"
    else:
        git_id_msg = ""

    # Generate git info text
    git_txt = f"# BOT STARTED\n"
    git_txt += f"```"
    git_txt += f"Branch:     {git_branch_local}\n"
    git_txt += f"\n"
    git_txt += f"Commit IDs:         {git_id_msg}\n     local: {git_id_local}\n    remote: {git_id_remote}\n"
    git_txt += f"\n"
    git_txt += f"Commit Description:\n"
    git_txt += f"   {git_commit_desc}\n"
    git_txt += f"```\n"
    git_txt += f"### Diff List:\n"
    git_txt += f"```"
    git_txt += f"{git_diff_list if git_diff_list else ' No changes.'}"
    git_txt += f"```"

    # Send git info text to log channel
    await send_log(None, f"{git_txt}")

    # Start loop for checking tournaments
    check_tournaments.start()

@tasks.loop(seconds=15)
async def check_tournaments():
    curr_time = math.floor(time.time())
    await check.ck_check_tournaments(bot, curr_time)


bot.run(TOKEN)
###############################################################################S