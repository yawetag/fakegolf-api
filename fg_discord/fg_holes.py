from discord.ext import commands

import fg_discord.fg_database as db
from fg_discord.fg_messages import send_user, send_channel
from fg_discord.fg_errors import error_notify

GOOD_REACTION = '👍'
BAD_REACTION = '❌'
UGLY_REACTION = '❓'
SWING_REACTION = '🏌️'

SWING_STATUS = 200

##### DISCORD FUNCTIONS #######################################################
class Holes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
            brief="Submit a shot.",
            description="-shoot <number>\nSubmit a shot with <number> as your guess.",
            aliases=['shot']
    )
    @commands.dm_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def shoot(self, ctx, shot=None):
        # First, let's get the user info
        user_info = db.generic_get_all_match_exact('users', 'discord_snowflake', ctx.author.id)
        if len(user_info) == 0:
            user_msg = "You are not in my database."
            await ctx.message.add_reaction(UGLY_REACTION)
            await ctx.reply(user_msg)
            return
        user_info = user_info[0]
        
        # Now that we have the user info, let's see if they have a shot waiting.
        user_shot_id = db.generic_get_all_match_exact('tournament_status', 'user_id', user_info['id'])
        if len(user_shot_id) == 0:
            user_msg = "You are not currently in a tournament."
            await ctx.message.add_reaction(UGLY_REACTION)
            await ctx.reply(user_msg)
            return
        user_shot_id = user_shot_id[0]
        
        if user_shot_id['status_id'] != SWING_STATUS:
            user_msg = "It is not time to swing."
            await ctx.message.add_reaction(BAD_REACTION)
            await ctx.reply(user_msg)
            return

        if shot == None:                # If no number was submitted
            user_msg = "You did not submit a guess. You must submit an integer between 1 and 1000 inclusive."
            await ctx.message.add_reaction(BAD_REACTION)
            await ctx.reply(user_msg)
            return
        
        if not shot.isdigit():          # If shot was not an integer
            user_msg = "You did not submit an integer. You must submit an integer between 1 and 1000 inclusive."
            await ctx.message.add_reaction(BAD_REACTION)
            await ctx.reply(user_msg)
            return
        
        shot = int(shot)                # Since we know it's an integer now, let's make it one
        
        if shot < 1 or shot > 1000:     # If shot was outside the allowed numbers
            user_msg = "You did not submit a proper guess. You must submit an integer between 1 and 1000 inclusive."
            await ctx.message.add_reaction(BAD_REACTION)
            await ctx.reply(user_msg)
            return
        
        # It appears this is a correct shot by a user who needs to enter a shot, so let's store it and change their status
        # First, store the swing in shot_log
        store_swing = db.holes_insert_swing_in_shot_log(user_shot_id['shot_id'], shot)

        # Second, update the user's status to waiting on result
        update_status = db.holes_change_shot_status(user_shot_id['id'], 300)

        # Lastly, emote the message to show it was received
        await ctx.message.add_reaction(SWING_REACTION)
###############################################################################

async def setup(bot):
    await bot.add_cog(Holes(bot))