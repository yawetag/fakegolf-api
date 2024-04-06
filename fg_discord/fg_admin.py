from discord.ext import commands

import keys

##### ADMIN GLOBAL VARIABLES ##################################################
ADMIN_ROLE = keys.admin_role
###############################################################################

##### DISCORD FUNCTIONS #######################################################
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
###############################################################################

async def setup(bot):
    await bot.add_cog(Admin(bot))