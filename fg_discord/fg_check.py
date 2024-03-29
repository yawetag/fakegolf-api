import asyncio
import discord
import requests

from datetime import datetime
from discord.ext import commands

import fg_discord.fg_database as db
from fg_discord.fg_messages import send_user, send_channel
from fg_discord.fg_errors import error_notify

async def ck_check_tournaments(s):
    """Checks status of tournaments."""
    dt = datetime.fromtimestamp(s)
    print()
    print(f"[{dt.strftime('%Y-%m-%d %H:%M:%S')} | {s}] Checking tournaments...")
    
    return


##### DISCORD FUNCTIONS #######################################################
class Checks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
###############################################################################

async def setup(bot):
    await bot.add_cog(Checks(bot))