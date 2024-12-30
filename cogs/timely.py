import disnake
from disnake.ext import commands
from untils.databases import UsersDataBase
from untils.databasesTime import CooldownDatabase
import datetime
from datetime import datetime, timedelta
import asyncio
emoji = ""
import random 

class Timely(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = UsersDataBase()
        self.db_time = CooldownDatabase()

    @commands.slash_command(name='timely', description='Нагорода кожні 12 годин')
    async def timely(self, inter):
        member = inter.author
        await self.db.create_table()
        await self.db.add_user(member)
        user_data = await self.db.get_user(member)
        await self.db_time.create_table()
        await self.db_time.get_cooldown(inter.author.id)
        cooldown = await self.db_time.check_cooldown(inter.author.id)
        if cooldown.total_seconds() > 0:
            hours, remainder = divmod(cooldown.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            embed = disnake.Embed(color=0x2F3136)
            server_avatar_url = inter.guild.icon.url if inter.guild.icon else None
            embed.set_author(name="Cat | Timely", icon_url=server_avatar_url)
            embed.description = f'> Ви вже використовували команду, приходьте через {hours} годин та {minutes} хвилин'
            embed.set_thumbnail(url=member.display_avatar.url)
            await inter.response.send_message(embed=embed)
        else:
            amount = random.randint(5, 80)
            await self.db.update_money(member, amount)
            embed = disnake.Embed(color=0x2F3136)
            server_avatar_url = inter.guild.icon.url if inter.guild.icon else None
            embed.set_author(name="Cat | Timely", icon_url=server_avatar_url)
            embed.description = f'> {member.mention} ваш бонус на сьогодні : **{amount}** {emoji}'
            embed.set_thumbnail(url=member.display_avatar.url)
            await inter.response.send_message(embed=embed)
            timely_date = datetime.now().isoformat() 
            await self.db_time.set_cooldown(inter.author.id, timely_date)
            
            
             

def setup(bot):
    bot.add_cog(Timely(bot))
