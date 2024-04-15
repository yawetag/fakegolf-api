from dhooks import Webhook
from discord.ext import commands

import keys

async def send_announcement(ctx, message):
    """Sends announcement message to announcement channel."""
    hook = Webhook(keys.announcement_webhook)
    hook.send(message)

async def send_channel(ctx, message):
    """Sends discord message to channel."""
    await ctx.send(f"{ctx.author.mention} : {message}")

async def send_error(ctx, message):
    """Sends error message to error channel."""
    hook = Webhook(keys.error_webhook)
    hook.send(message)

async def send_log(ctx, message):
    """Sends log message to log channel."""
    hook = Webhook(keys.log_webhook)
    hook.send(message)

async def send_snow(ctx, snowflake, message):
    """Sends user a message through Discord snowflake."""
    user = ctx.get_user(int(snowflake))
    dm_chan = await user.create_dm()
    await dm_chan.send(message)

async def send_user(ctx, message):
    """Sends discord private message to user."""
    await ctx.author.send(f"{ctx.author.mention} : {message}")

##### DISCORD FUNCTIONS #######################################################
class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
###############################################################################

async def setup(bot):
    await bot.add_cog(Messages(bot))