from discord.ext import commands

import fg_discord.fg_database as db
from fg_discord.fg_messages import send_user, send_channel
from fg_discord.fg_errors import error_notify

##### DISCORD FUNCTIONS #######################################################
class Players(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def p_add_user(self, ctx):
        """Adds new user to the database."""
        user = db.players_add_user_by_discord_id(ctx)   # Add user to database
        if user:            # If user was added successfully, return id
            return user
        else:               # If not, return an error
            return 0
    
    def p_change_name(self, ctx, new_name):
        """Changes name of user in the database. Name must be less than 40 characters."""
        if len(new_name) < 1:
            return 0
        elif len(new_name) > 40:
            return 40
        
        user = db.players_change_name_by_discord_id(ctx, new_name)  # Change user in database
        if user:
            return 1
        else:
            return 2

    def p_is_user(self, ctx):
        """Checks database to see if user is active."""
        user = db.generic_get_all_match_exact('users', 'discord_snowflake', ctx.author.id)     # Get user from database
        if len(user) == 0:      # If no user was found, return None
            return None
        elif len(user) == 1:    # If user was found, return their info
            return user[0]
        else:                   # All other cases, return an error
            return 0

    @commands.command(
            brief="See your user info.",
            description="-info\nSee your Fake Golf user info.",
            aliases=['p_info']
    )
    async def info(self, ctx):
        user = Players.p_is_user(self, ctx)
        if user is None:
            message = "You have not joined. Type `-join` to join Fake Golf."
        elif user == 2:
            error_notify(ctx, "players.info", "PLAYER001")        
            message = "There has been an error in your command. Admins will look into it and contact you."
        else:
            message = f"Your player name is: {user['player_name']}\nTo change it, type `-name <new name>`."
        await send_channel(ctx, message)

    @commands.command(
            brief="Join Fake Golf as a user.",
            description="-join\nJoin Fake Golf as a user.",
            aliases=['p_join']
    )
    async def join(self, ctx):
        user = Players.p_is_user(self, ctx)
        if user is None:
            add_user = Players.p_add_user(self, ctx)
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
    
    @commands.command(
            brief="Change your player name.",
            description="-name <new name>\nChanges your player name to <new name>.\nName must be less than 40 characters.",
            aliases=['p_name']
    )
    async def name(self, ctx, *, player_name=""):
        user = Players.p_is_user(self, ctx)
        if user is None:
            message = "You have not joined. Type `-join` to join Fake Golf."
        elif user == 2:
            error_notify(ctx, "players.name", "PLAYER001")
            message = "There has been an error in your command. Admins will look into it and contact you."
        else:
            name = Players.p_change_name(self, ctx, player_name)
            if name == 0:
                message = "You must enter a new name: `-name <new name>`"
            elif name == 40:
                message = "Your new name cannot be longer than 40 characters."
            elif name == 2:
                error_notify(ctx, "players.name", "PLAYER003")
                message = "There has been an error in your command. Admins will look into it and contact you."
            else:
                message = f"Your name has been changed to: {player_name}"
            await send_channel(ctx, message)
###############################################################################

async def setup(bot):
    await bot.add_cog(Players(bot))