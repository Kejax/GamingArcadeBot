import discord
from discord.ext import commands, tasks
from views import *
import jenv

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="§$%", intents=intents)
bot.is_ready_v = True
bot.presence = 0
bot.activities = [
    discord.Game("Minecraft"),
    discord.Game("Hypixel Bed Wars"),
    discord.Game("Don't Starve"),
    discord.Streaming(name="Yuri1037", url="https://twitch.tv/yuri1037"),
    discord.Game("mit Berechtigungen")
]


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    if bot.is_ready_v:

        extensions = [
            "cogs.moderator"
        ]

        for extension in extensions:
            await bot.load_extension(extension)

        # Do things, after the bot is ready
        activity_loop.start()
        bot.is_ready_v = False
        await bot.tree.sync()


@tasks.loop(seconds=10)
async def activity_loop():
    if bot.presence >= len(bot.activities):
        bot.presence = 0
    await bot.change_presence(activity=bot.activities[bot.presence], status=discord.Status.online)
    bot.presence += 1


@bot.tree.command(name="ping")
async def ping_cmd(interaction: discord.Interaction):
    embed = discord.Embed(description=f"Current Ping: {round(bot.latency * 1000, 2)}", color=discord.Color.green())
    await interaction.response.send_message(embed=embed)


@bot.tree.context_menu(name="Nachricht melden")
async def report_message_ctx_menu(interaction: discord.Interaction, message: discord.Message) -> None:
    embed = discord.Embed(description="Nachricht melden?", color=discord.Color.blue())
    confirm_view = ReportMessageView(message=message)
    await interaction.response.send_message(embed=embed, view=confirm_view, ephemeral=True)
    await confirm_view.wait()
    if confirm_view.value:
        log_channel = interaction.guild.get_channel(829706368754647071)
        embed = discord.Embed(title="Message Report")
        if message.content:
            embed.description = message.content
        embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
        embed.timestamp = message.created_at
        url_view = discord.ui.View()
        url_view.add_item(discord.ui.Button(label="Zur Message", style=discord.ButtonStyle.url, url=message.jump_url))
        await log_channel.send(embed=embed)


if __name__ == "__main__":
    mode = input("Please enter the mode, the bot should run in:\n (p)roduction or (d)eveloping")
    if mode.upper().lower() == "p":
        bot.run(jenv.getenv("TOKEN"))
    elif mode.upper().lower() == "d":
        bot.run(jenv.getenv("DEV_TOKEN"))
    else:
        print("Aborting due a not valid mode")
