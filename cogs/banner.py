import disnake
from disnake.ext import commands


class Banner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  

    
    @commands.slash_command(description="Подивитися баннер юзеру")  
    async def banner(self, interaction, member: disnake.Member = commands.Param(lambda i: i.author, name="юзер", description="Юзер, баннер якого треба подивитись")):
        member = member or interaction.author  
        user = await self.bot.fetch_user(member.id)  
        guild = interaction.guild  

        
        if user.banner is None:
            # Отправляем сообщение о отсутствии баннера
            await interaction.response.send_message("У цього юзера нема баннеру!", ephemeral=True)
        else:
            embed = disnake.Embed(color=0x2F3136)  
            embed.set_image(url=user.banner)  
            embed.set_author(name="Баннер юзера", icon_url=guild.icon.url)  
            await interaction.response.send_message(embed=embed)  


def setup(bot):
    bot.add_cog(Banner(bot))