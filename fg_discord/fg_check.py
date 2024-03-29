import asyncio
import discord
import requests

from datetime import datetime
from discord.ext import commands

import fg_discord.fg_database as db
from fg_discord.fg_messages import send_announcement, send_channel, send_log, send_user
from fg_discord.fg_errors import error_notify

async def ck_check_tournaments(ts):
    """Checks status of tournaments."""
    dt = datetime.fromtimestamp(ts)
    codes = db.get_tournament_statuses()
    c = {obj['id']:obj for obj in codes}

    t_list = db.get_tournaments_with_status()


    print()
    print(f"[{dt.strftime('%Y-%m-%d %H:%M:%S')} | {ts}] Checking tournaments...")

    # For each status, run the appropriate check for it
    await ck_tourn_201(ts, c, t_list)
    
    return

async def ck_tourn_201(ts, c, t_list):
    """
    Tournament Status 201 Check.
    If the current time is past the `start_time`:
        * Change the status to 210
        * Announce the tournament has started
    If not, keep status at 201
    """
    ci = c[201]
    
    print(f"   Checking status {ci['id']} - {ci['status_name']}")

    for t in t_list:
        if t['status_id'] == ci['id']:
            if int(t['start_time']) <= ts:  # If the start time has passed, do some work
                db.change_tournament_status(t['id'], ci['next_status'])     # Change to next code
                log_msg = f"<t:{ts}:T> **{t['tournament_name']}** [{t['id']}] status change: **{ci['id']} → {ci['next_status']}** | {ci['status_name']} → {c[ci['next_status']]['status_name']}"
                ann_msg = f"### TOURNAMENT OPEN FOR REGISTRATION\n**{t['tournament_name']}** by *{t['player_name']}* has opened for registration. Type `.tournament_info {t['id']}` for more information or `.join_tournament {t['id']}` to join."
                await send_log(None, log_msg)           # Send change to log channel
                await send_announcement(None, ann_msg)  # Send announcement to announcements channel

##### DISCORD FUNCTIONS #######################################################
class Checks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
###############################################################################

async def setup(bot):
    await bot.add_cog(Checks(bot))