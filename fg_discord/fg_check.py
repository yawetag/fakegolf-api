from datetime import datetime
from discord.ext import commands

import keys

import fg_discord.fg_database as db
from fg_discord.fg_messages import send_announcement, send_channel, send_log, send_snow, send_user
from fg_discord.fg_errors import error_notify

##### CONSTANT VARIABLES ######################################################
GUILD_ID = keys.guild_id
###############################################################################

async def ck_check_tournaments(bot, ts):
    """Checks status of tournaments."""
    dt = datetime.fromtimestamp(ts)
    codes = db.get_tournament_statuses()
    c = {obj['id']:obj for obj in codes}

    t_list = db.get_tournaments_with_status()


    print()
    print(f"[{dt.strftime('%Y-%m-%d %H:%M:%S')} | {ts}] Checking tournaments...")

    # For each status, run the appropriate check for it
    await ck_tourn_201(bot, ts, c, t_list)
    await ck_tourn_210(bot, ts, c, t_list)
    await ck_tourn_250(bot, ts, c, t_list)
    await ck_tourn_252(bot, ts, c, t_list)
    await ck_tourn_254(bot, ts, c, t_list)
    await ck_tourn_256(bot, ts, c, t_list)
    await ck_tourn_258(bot, ts, c, t_list)
    
    return

async def ck_tourn_201(bot, ts, c, t_list):
    """
    Tournament Status 201 Check.
    If the current time is past the `start_time`:
        * Change the status to next status
        * Announce the tournament has started
    If not, keep status
    """
    ci = c[201]
    
    await print_log(ci)
    
    for t in t_list:
        if t['status_id'] == ci['id']:
            if int(t['start_time']) <= ts:  # If the start time has passed, do some work
                db.change_tournament_status(t['id'], ci['next_status'])     # Change to next code
                msg = f"### TOURNAMENT OPEN FOR REGISTRATION\n**{t['tournament_name']}** by *{t['player_name']}* has opened for registration. Type `-tournament_info {t['id']}` for more information or `-join_tournament {t['id']}` to join."
                await log_msg(ts, t, ci, c)
                await ann_msg(msg)

async def ck_tourn_210(bot, ts, c, t_list):
    """
    Tournamnent Status 210 Check.
    If the current time is past the `end_time`:
        * Change the status to next status
    If not, keep status
    """
    ci = c[210]

    await print_log(ci)

    for t in t_list:
        if t['status_id'] == ci['id']:
            if int(t['end_time']) <= ts: # If the end time has passed, do some work
                db.change_tournament_status(t['id'], ci['next_status'])     # Change to next code
                await log_msg(ts, t, ci, c)

async def ck_tourn_250(bot, ts, c, t_list):
    """
    Tournament Status 250 Check.
    Simply moves status to next status
    """
    ci = c[250]

    await print_log(ci)

    for t in t_list:
        if t['status_id'] == ci['id']:
            db.change_tournament_status(t['id'], ci['next_status'])         # Change to next code
            await log_msg(ts, t, ci, c)

async def ck_tourn_252(bot, ts, c, t_list):
    """
    Tournament Status 252 Check.
    For each user in a tournament, check they are still in the server.
    If they aren't, remove them from the tournament.
    Afterward, move status to next status.
    """
    ci = c[252]

    await print_log(ci)

    guild = bot.get_guild(GUILD_ID)

    for t in t_list:
        if t['status_id'] == ci['id']:
            reg_users = db.get_tournament_user_info(t['id'])
            for r in reg_users:
                if guild.get_member(int(r['discord_snowflake'])) is None:    # If user is not active in server, remove them.
                    rem_user = db.remove_user_from_tournament(t['id'], r['id'])
                    log_ms = f"<t:{ts}:T> **{t['tournament_name']}** [{t['id']}] Inactive User: **{r['id']} - <@{r['discord_snowflake']}>** | Removed from tournament."
                    await send_log(None, log_ms)
            
            db.change_tournament_status(t['id'], ci['next_status'])         # Change to next code
            await log_msg(ts, t, ci, c)

async def ck_tourn_254(bot, ts, c, t_list):
    """
    Tournament Status 254 Check.
    For each user in a tournament, check they are not banned.
    If they are, remove them from the tournament.
    Afterward, move status to next status.
    """
    ci = c[254]

    await print_log(ci)

    for t in t_list:
        if t['status_id'] == ci['id']:
            reg_users = db.get_tournament_user_info(t['id'])
            for r in reg_users:
                if r['is_banned'] == 1:     # If user is banned from playing, remove them.
                    rem_user = db.remove_user_from_tournament(t['id'], r['id'])
                    log_ms = f"<t:{ts}:T> **{t['tournament_name']}** [{t['id']}] Banned User: **{r['id']} - <@{r['discord_snowflake']}>** | Removed from tournament."
                    await send_log(None, log_ms)
            
            db.change_tournament_status(t['id'], ci['next_status'])         # Change to next code
            await log_msg(ts, t, ci, c)

async def ck_tourn_256(bot, ts, c, t_list):
    """
    Tournament Status 256 Check.
    For each user in a tournament, check they are not in another tournament.
    If they are, remove them from the tournament.
    Afterward, move status to the next status.
    """
    ci = c[256]

    await print_log(ci)

    for t in t_list:
        if t['status_id'] == ci['id']:
            reg_users = db.get_tournament_user_info(t['id'])
            for r in reg_users:
                    num_games = db.get_tournament_user_games(r['id'])
                    if len(num_games) > 1:      # If user is registered in multiple tournaments, remove them.
                        rem_user = db.remove_user_from_tournament(t['id'], r['id'])
                        log_ms = f"<t:{ts}:T> **{t['tournament_name']}** [{t['id']}] User in Multiple Tournaments: **{r['id']} - <@{r['discord_snowflake']}>** | Removed from tournament."
                        await send_log(None, log_ms)
            
            db.change_tournament_status(t['id'], ci['next_status'])         # Change to next code
            await log_msg(ts, t, ci, c)

async def ck_tourn_258(bot, ts, c, t_list):
    """
    Tournament Status 258 Check.
    Check that the tournament has an active player.
    If not, notify the tournament organizer and move to completed.
    If so, move status to the next status.
    """
    ci = c[258]

    await print_log(ci)

    for t in t_list:
        if t['status_id'] == ci['id']:
            reg_users = db.get_tournament_user_info(t['id'])
            if len(reg_users) == 0:
                log_ms = f"<t:{ts}:T> **{t['tournament_name']}** [{t['id']}] No one registered for tournament | Moved to Canceled."
                await send_log(None, log_ms)

                note_ms = f"**{t['tournament_name']}** has no active players, so it has been canceled."
                await send_note(bot, t['discord_snowflake'], note_ms)

                db.change_tournament_status(t['id'], 890)                   # Change to canceled
                ci['next_status'] = 890
                await log_msg(ts, t, ci, c)
            else:
                db.change_tournament_status(t['id'], ci['next_status'])     # Change to next code
                await log_msg(ts, t, ci, c)

async def ann_msg(msg):
    """Sends message to announcements channel."""

    await send_announcement(None, msg)  # Send announcement to announcements channel

async def log_msg(ts, t, ci, c):
    """Sends log to log channel."""

    log_msg = f"<t:{ts}:T> **{t['tournament_name']}** [{t['id']}] Status Change: **{ci['id']} → {ci['next_status']}** | {ci['status_name']} → {c[ci['next_status']]['status_name']}"
    await send_log(None, log_msg)           # Send change to log channel

async def send_note(bot, u, msg):
    """Sends message to discord snowflake."""

    await send_snow(bot, u, msg)

async def print_log(ci):
    """Prints log to screen."""

    print(f"   Checking status {ci['id']} - {ci['status_name']}")


##### DISCORD FUNCTIONS #######################################################
class Checks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
###############################################################################

async def setup(bot):
    await bot.add_cog(Checks(bot))