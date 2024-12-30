import disnake 
from disnake.ext import commands
import datetime

class Arrole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Додати або зняти роль у юзера")
    async def arrole(self, inter, member: disnake.Member = commands.Param(description='Треба вибрати юзера'), role: disnake.Role = commands.Param(description='Треба вибрати роль')):
        if role.position > inter.author.top_role.position:
            return await inter.response.send_message('You cannot give roles higher than your top role.', ephemeral=True)
        if role.position > inter.guild.me.top_role.position:
            return await inter.response.send_message('I cannot give roles higher than my top role.', ephemeral=True)
        if role in member.roles:
            await member.remove_roles(role)
            server_avatar_url = inter.guild.icon.url if inter.guild.icon else disnake.Embed.Empty
            embed = disnake.Embed(color=0x2F3136, timestamp=datetime.datetime.now())
            embed.set_author(name="Cat | Arrole", icon_url=server_avatar_url)
            embed.set_thumbnail(url=inter.author.display_avatar.url)
            embed.description = f"Ви успішно зняли роль: {role.mention} у пользователя {member.mention}"
            await inter.response.send_message(embed=embed)
        else:
            await member.add_roles(role)
            server_avatar_url = inter.guild.icon.url if inter.guild.icon else disnake.Embed.Empty
            embed = disnake.Embed(color=0x2F3136, timestamp=datetime.datetime.now())
            embed.set_author(name="Cat | Arrole", icon_url=server_avatar_url)
            embed.set_thumbnail(url=inter.author.display_avatar.url)
            embed.description = f"Ви успішно додали роль: {role.mention} юзеру {member.mention}"
            await inter.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(Arrole(bot))
 



        