import disnake
from disnake.ext import commands, tasks
import asyncio
from untils.databases import UsersDataBase
from untils.databasesMarry import MarryDatabase
amount = 1


class VoiceActivity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = UsersDataBase()  
        self.marry_db = MarryDatabase()
        self.voice_members = {}  

    @tasks.loop(seconds=5.0)
    async def check_voice_activity(self):
        for member in self.voice_members.keys():
            if member.voice and member.voice.channel: 
                await self.db.create_table()
                await self.db.add_user(member) 
                user = await self.db.get_user(member)  
                
                
                marry_data = await self.marry_db.get_user(member)
                if marry_data and member.voice.channel.name == marry_data[5]:  
                    
                    partner_id = marry_data[1]  
                    partner = member.guild.get_member(partner_id)
                    
                    
                    if partner and partner.voice and partner.voice.channel and partner.voice.channel == member.voice.channel:
                        
                        await self.marry_db.update_voice_time(member.id, 5)
                
                if user:
                    await self.db.update_voice_time(member.id, 5)  
                    await self.db.update_experience(member, 5)
                    await self.db.check_level_up(member)
            else:
                self.voice_members.pop(member, None)
                await self.db.commit()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: disnake.Member, before: disnake.VoiceState,
                                    after: disnake.VoiceState):
        if before.channel is None:  
            self.voice_members[member] = True
            if not self.check_voice_activity.is_running():
                self.check_voice_activity.start()
        elif after.channel is None:
            self.voice_members.pop(member, None)
            if not self.voice_members and self.check_voice_activity.is_running():
                self.check_voice_activity.stop()



 



    @commands.slash_command(name='online', description='Посмотреть онлайн юзера')
    async def online(self, interaction, member: disnake.Member = (commands.Param(description='Треба вибрати юзера', default=None))): 
        await self.db.create_table()  
        if not member:
            member = interaction.author
        await self.db.add_user(member)  
        user = await self.db.get_user(member)  
        if user is not None:
            seconds = user[2]
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            embed = disnake.Embed(color=0x2F3136)
            embed.add_field(name=f'⠀', value=f'>>> Онлайн юзера {member.mention}: **{hours}** годин **{minutes}** хвилин **{seconds}** секунд')
            embed.set_thumbnail(url=member.display_avatar.url)
            await interaction.response.send_message(embed=embed)  


def setup(bot):
    bot.add_cog(VoiceActivity(bot))                         
