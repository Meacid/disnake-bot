import disnake
from disnake.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def ping(self, interaction: disnake.CommandInteraction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"`🏓 Понг! Задержка бота: {latency}мс`")

def setup(bot):
    bot.add_cog(Ping(bot))
