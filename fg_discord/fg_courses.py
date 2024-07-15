from discord.ext import commands

import fg_discord.fg_database as db
from fg_discord.fg_messages import send_user, send_channel
from fg_discord.fg_errors import error_notify

##### DISCORD FUNCTIONS #######################################################
class Courses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def c_get_courses(self):
        courses = db.check_get_all_courses()  # Get list of courses
        if courses is None:
            return 0
        else:
            return courses
    
    @commands.command(
            brief="See list of courses.",
            description="-courses\nSee list of courses in Fake Golf.",
            aliases=['c_list']
    )
    async def courses(self, ctx):
        courses = Courses.c_get_courses(self)
        if courses == 0:
            await error_notify(ctx, "courses.courses", "COURSES001")
            message = "There has been an error in your command. Admins will look into it and contact you."
        else:
            message = f"Here is a list of courses:\n"
            for c in courses:
                message += f"   (#{c['id']}) **{c['course_name']}** by {c['player_name']}. Par {c['par']}. {c['yardage']:,} yards.\n"
        message += "\nFor more information on a course, type `-course_info <#>`, where `<#>` is the course number."

        await send_channel(ctx, message)

###############################################################################

async def setup(bot):
    await bot.add_cog(Courses(bot))