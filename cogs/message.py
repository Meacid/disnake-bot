import disnake
from disnake.ext import commands
from untils.databases import UsersDataBase

class MessageCounter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = UsersDataBase()  

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot:
            return
        
        await self.db.create_table()
        await self.db.add_user(message.author)
        await self.db.update_message_count(message.author, 1)
        await self.db.update_experience(message.author, 5)
        await self.db.check_level_up(message.author)

def setup(bot):
    bot.add_cog(MessageCounter(bot))