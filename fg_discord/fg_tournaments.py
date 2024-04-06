import asyncio
import discord
import requests

from discord.ext import commands

import fg_discord.fg_database as db
from fg_discord.fg_messages import send_user, send_channel
from fg_discord.fg_errors import error_notify

##### DISCORD FUNCTIONS #######################################################
class Tournaments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def t_get_tournaments(self):
        tournaments = db.get_all_tournaments()  # Get list of tournaments
        if tournaments is None:
            return 0
        else:
            return tournaments
    
    def t_tournament_info(self, tid):
        """Gets information about a tournament."""
        tournaments = db.get_tournament_info(tid)
        if tournaments is None:
            return 0
        else:
            return tournaments
    
    def t_tournament_organizer(self, tid):
        """Gets Discord id of the tournament organizer."""
        organizer = db.get_tournament_organizer(tid)
        if organizer is None:
            return 0
        else:
            return organizer[0]['discord_snowflake']
    
    def t_tournament_status(self, tid):
        """Gets status id of tournament."""
        status = db.get_tournament_status(tid)
        if status is None:
            return 0
        else:
            return status[0]['status_id']
    
    def t_tournament_list_by_user(self, ctx):
        """Gets list of tournaments for user."""
        tournaments = db.get_tournament_list_by_user(ctx)
        if tournaments is None:
            return 0
        else:
            return tournaments
    
    def t_tournament_register(self, ctx, tid):
        """Registers a user for a tournament."""

        # Get users.id by snowflake
        userid = db.get_user_by_discord_id(ctx.author.id)
        register = db.add_user_to_tournament(userid[0]['id'], tid)
        if register:
            return register
        else:
            return 0
    
    @commands.command(
            brief="See list of tournaments.",
            description="-tournaments\nSee list of tournaments in Fake Golf.",
            aliases=['t_list']
    )
    async def tournaments(self, ctx):
        tournaments = Tournaments.t_get_tournaments(self)
        if tournaments == 0:
            await error_notify(ctx, "tournaments.tournaments", "TOURNAMENTS001")
            message = "There has been an error in your command. Admins will look into it and contact you."
        else:
            message = f"Here is a list of tournaments:\n"
            for t in tournaments:
                message += f"   (#{t['id']}) **{t['tournament_name']}** by {t['player_name']}. "
                message += f"{t['rounds']} {'round' if t['rounds']==1 else 'rounds'}. "
                message += f"{t['status_name']}, closes <t:{t['end_time']}:R> (<t:{t['end_time']}:f> in your timezone)"
                message += f"\n"
        message += "\nFor more information on a tournament, type `-tournament_info <#>`, where `<#>` is the tournament number."
        message += "\nTo join a tournament, type `-join_tournament <#>` where `<#>` is the tournament number."

        await send_channel(ctx, message)

    @commands.command(
        brief="See detail of tournament.",
        description="-tournament_info <number>\nSee details of tournament by number.",
        aliases=['t_info']
    )
    async def tournament_info(self, ctx, tournament_id=0):
        tournament = Tournaments.t_tournament_info(self, tournament_id)
        if tournament == 0:
            await error_notify(ctx, "tournaments.tournament_info", "TOURNAMENTS001")
            message = "There has been an error in your command. Admins will look into it and contact you."
        elif len(tournament) == 0:
            message = "There are no tournaments matching that id. Please type `-tournaments` to see all active tournaments."
        else:
            message = f"Here is information on **{tournament[0]['tournament_name']}** by {tournament[0]['player_name']}:\n"
            message += f"Description: {tournament[0]['description']}\n"
            for t in tournament:
                message += f"   Round {t['round']}: **{t['course_name']}** "
                message += f"(par: {t['par']}. yards: {t['yardage']:,}). "
                message += f"Runs <t:{t['start_time']}:D> to <t:{t['end_time']}:D>.\n"
            message += f"To join the tournament, type `-join_tournament {tournament_id}`"
        await send_channel(ctx, message)
    
    @commands.command(
        brief="Join a tournament.",
        description="-join_tournament <number>\nJoin the tournament by number.",
        aliases=['t_join', 'tournament_join']
    )
    async def join_tournament(self, ctx, tournament_id=0):
        organizer = Tournaments.t_tournament_organizer(self, tournament_id)
        status = Tournaments.t_tournament_status(self, tournament_id)
        user_tourn = Tournaments.t_tournament_list_by_user(self, ctx)
        if organizer == str(ctx.author.id):    # If user is the organizer of the tournament, they can't join
            message = "You are the tournament organizer. You cannot join your own tournament."
        elif status not in [210]: # If the tournament is not open for registration, they can't join
            message = "This tournament is not open for registration."
        elif len(user_tourn) > 0:    # If the user is already in a tournament, they can't join
            message = "You are already playing in a tournament. You can only play one tournament at a time."
        else:
            register = Tournaments.t_tournament_register(self, ctx, tournament_id)
            tournament = Tournaments.t_tournament_info(self, tournament_id)
            message = f"You have entered **{tournament[0]['tournament_name']}**. Good luck!"
        await send_channel(ctx, message)
        
###############################################################################

async def setup(bot):
    await bot.add_cog(Tournaments(bot))