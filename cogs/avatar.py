import disnake
from disnake.ext import commands

class Avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description='Подивитися аватар юзера')
    async def avatar(self, interaction, member: disnake.Member = commands.Param(description='Треба вибрати юзера із списку', default=None)):
        member = member or interaction.author
        embed = disnake.Embed(
            title=f"Аватар – {member}",
            color=0x2F3136
        )
        server = interaction.guild
        server_avatar_url = server.icon.url if server.icon else disnake.Embed.Empty
        embed.set_author(name="Cat | Аватар", icon_url=server_avatar_url)
        embed.set_image(url=member.display_avatar)
        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Avatar(bot))