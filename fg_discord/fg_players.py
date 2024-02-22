import asyncio
import discord
import requests

from discord.ext import commands

import fg_discord.fg_database as db
from fg_discord.fg_messages import send_user, send_channel
from fg_discord.fg_errors import error_notify

##### DISCORD FUNCTIONS #######################################################
class Players(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def add_user(self, ctx):
        """Adds new user to the database."""
        user = db.add_user_by_discord_id(ctx)   # Add user to database
        if user:            # If user was added successfully, return id
            return user
        else:               # If not, return an error
            return 0

    def is_user(self, ctx):
        """Checks database to see if user is active."""
        user = db.get_user_by_discord_id(ctx.author.id)     # Get user from database
        if len(user) == 0:      # If no user was found, return None
            return None
        elif len(user) == 1:    # If user was found, return their info
            return user[0]
        else:                   # All other cases, return an error
            return 0
    
    @commands.command(
            brief="Join Fake Golf as a user.",
            description="-join\nJoin Fake Golf as a user."
    )
    async def join(self, ctx):
        user = Players.is_user(self, ctx)
        if user is None:
            add_user = Players.add_user(self, ctx)
            if add_user == 0:
                error_notify(ctx, "players.join", "PLAYER001")
                message = "There has been an error in your command. Admins will look into it and contact you."
            else:
                message = "Welcome to the game! Type `-info` to view your player info."
        elif user == 2:
            error_notify(ctx, "players.join", "PLAYER001")
            message = "There has been an error in your command. Admins will look into it and contact you."
        else:
            message = "You have already joined the game. Type `-info` to view your player info."
        await send_channel(ctx, message)
###############################################################################

async def setup(bot):
    await bot.add_cog(Players(bot))