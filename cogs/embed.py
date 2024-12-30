import disnake
from disnake.ext import commands

class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description='Кастомный эмбед')
    @commands.has_permissions(administrator=True)
    async def embed(self, interaction):
        embed = disnake.Embed(title="Название эмбеда", description="Описание эмбеда", color=0x00ff00)
        embed.add_field(name="Название поля 1", value="Значение поля 1", inline=False)
        embed.add_field(name="Название поля 2", value="Значение поля 2", inline=False)
        embed.add_field(name="Название поля 3", value="Значение поля 3", inline=False)
        embed.set_footer(text="Нижний колонтитул")
        embed.set_author(name="Автор эмбеда")
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_image(url=None)
        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Embed(bot))