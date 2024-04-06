from discord.ext import commands
from fg_discord.fg_errors import error_notify

##### DISCORD FUNCTIONS #######################################################
class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @commands.command()
    async def yawetag(self, ctx):
        await ctx.send(f"YAWETAG!")
    
    @commands.command()
    async def test_error(self, ctx):
        await error_notify(ctx, "players.join", "PLAYER002")

###############################################################################

async def setup(bot):
    await bot.add_cog(Test(bot))