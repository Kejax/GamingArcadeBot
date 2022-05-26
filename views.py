import discord


class ReportMessageView(discord.ui.View):

    def __init__(self, message: discord.Message):
        super().__init__()
        self.value = None
        self.message: discord.Message = message

    @discord.ui.button(label="Bestätigen", style=discord.ButtonStyle.green)
    async def confirm_report(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(description=f"Die Nachricht von {self.message.author} wurde gemeldet", color=discord.Color.green())
        await interaction.edit_original_message(embed=embed, view=None, ephemeral=True)
        self.value = True
        self.stop()

    @discord.ui.button(label="Abbrechen", style=discord.ButtonStyle.red)
    async def abort_report(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(description=f"Dein Report wurde abgebrochen")
        await interaction.edit_original_message(embed=embed, view=None, ephemeral=True)
        self.value = True
        self.stop()
