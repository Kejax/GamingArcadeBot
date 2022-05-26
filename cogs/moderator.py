import discord
from discord import app_commands
from discord.ext import commands, tasks
import time
import datetime
import pytz


class Moderator(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        """self.report_message_menu = app_commands.ContextMenu(
            name="Nachricht melden",
            callback=self.report_message_ctx_menu
        )
        self.bot.tree.add_command(self.report_message_menu)"""

    async def cog_load(self):
        self.remember_yuri_loop.start()

    @app_commands.command(name="userinfo", description="Returns information's about the given user")
    async def userinfo_cmd(self, interaction: discord.Interaction, user: discord.Member):
        """Provides information's about the user"""
        if user is None:
            user = interaction.user
        embed = discord.Embed(title=f"Userinfo - {user}", description=user.mention, color=user.accent_color)
        embed.add_field(name="Nickname", value=user.nick, inline=False)
        embed.add_field(name="Joined Guild", value=f"<t:{str(time.mktime(user.joined_at.timetuple()))[:-2]}:F>", inline=False)
        embed.add_field(name="Joined Discord", value=f"<t:{str(time.mktime(user.created_at.timetuple()))[:-2]}:F>", inline=False)
        roles = str()
        for role in user.roles:
            if role != user.guild.default_role:
                roles = roles + role.mention
        if len(roles) > 300:
            roles = "Too many to show"
        roles_len = len(user.roles) - 1
        embed.add_field(name=f"Roles [{roles_len}]", value=roles, inline=False)
        embed.set_thumbnail(url=user.avatar.url)
        await interaction.response.send_message(embed=embed)

    @tasks.loop(time=[datetime.time(hour=15, minute=30, tzinfo=pytz.timezone("Europe/Berlin")), datetime.time(hour=19, tzinfo=pytz.timezone("Europe/Berlin"))])
    async def remember_yuri_loop(self):
        team_channel = self.bot.get_channel(896011380610699300)
        await team_channel.send("<@791432541939957762> Video hochladen!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Moderator(bot))
