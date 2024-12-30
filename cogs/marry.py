import disnake
import io
from PIL import Image, ImageDraw, ImageFont, ImageOps
from disnake.ext import commands, tasks
import asyncio
from untils.databases import UsersDataBase
from untils.databasesMarry import MarryDatabase
import requests   
from datetime import datetime

class Marry(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  
        self.user_db = UsersDataBase()  
        self.marry_db = MarryDatabase()
        self.temp_channels = {}
        self.voice_members = {} 
       

    @commands.slash_command(name="marry", description='Освідчитися')
    async def marry(self, inter, member: disnake.Member = (commands.Param(description='Треба вибрати юзера'))):
        if member.bot:
            await inter.response.send_message("Ви не можете освідчитися з ботом.", ephemeral=True)
            return

        if inter.author == member:
            await inter.response.send_message("Ви не можете освідчитися з самим собою.", ephemeral=True)
            return

        await self.user_db.create_table()
        await self.user_db.add_user(inter.author)
        await self.user_db.add_user(member)
        user = await self.user_db.get_user(inter.author)
        if user[1] < 2000:
            embed = disnake.Embed(color=0x2F3136)
            embed.description = f'{inter.author.mention} у вас нема коштів на здійснення освідчення.'
            await inter.response.send_message(embed=embed, ephemeral=True)
            return

        await self.user_db.update_money(inter.author,-2000)
        marriage_date = datetime.now().isoformat() 
        await self.marry_db.create_table()
        await self.marry_db.add_user(inter.author, member, marriage_date)
        ofcorsebutton = disnake.ui.Button(style=disnake.ButtonStyle.gray, label="Так", custom_id="ofcorsebutton")
        ofcorsenobutton = disnake.ui.Button(style=disnake.ButtonStyle.gray, label="Ні", custom_id="ofcorsenobutton")
        view = disnake.ui.View()
        view.add_item(ofcorsebutton)
        view.add_item(ofcorsenobutton)
        embed = disnake.Embed(color=0x2F3136)
        server_avatar_url = inter.guild.icon.url if inter.guild.icon else None
        embed.set_author(name="Cat | Освідчення", icon_url=server_avatar_url)
        embed.add_field(name=f'⠀', value=f'> {member.mention}, {inter.author.mention} хоче зробити вам освідчення, ви згодні?')
        marriage_date = datetime.now().isoformat()  
        embed.set_thumbnail(url=member.display_avatar.url)
        await inter.response.send_message(embed=embed, view=view)

    @commands.slash_command(name="divorce", description='Розірвати стосунки')
    async def divorce(self, inter):
        
        member_id = await self.marry_db.get_user(inter.author)

        
        if member_id is None:
            await inter.response.send_message("No relationship found for you.")
            return

        
        if len(member_id) < 2:
            await inter.response.send_message("Invalid relationship data.")
            return

        
        if inter.author.id == member_id[0]:
            member2_id = member_id[1]
        elif inter.author.id == member_id[1]:
            member2_id = member_id[0]
        else:
            await inter.response.send_message("You are not in a relationship.")
            return

        
        member1 = inter.guild.get_member(inter.author.id)
        member2 = inter.guild.get_member(member2_id)
        if member1 is None or member2 is None:
            await inter.response.send_message("Could not find one or both members.")
            return

        
        role = disnake.utils.get(inter.guild.roles, id=1229309971641143336)
        if role is not None:
            await member1.remove_roles(role)
            await member2.remove_roles(role)

        
        await self.marry_db.remove_user(inter.author)

        
        embed = disnake.Embed(color=0x2F3136)
        server_avatar_url = inter.guild.icon.url if inter.guild.icon else None
        embed.set_author(name="Cat | Divorce", icon_url=server_avatar_url)
        embed.add_field(name='⠀', value='> Ви успішно стали сігмою')
        await inter.response.send_message(embed=embed)



    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id == "ofcorsebutton":
            member_id = await self.marry_db.get_user(inter.author)
            if member_id:
                member = inter.guild.get_member(int(member_id[0]))
                member2 = inter.guild.get_member(int(member_id[1]))

                
                if inter.user.id == member2.id:
                    role = disnake.utils.get(member.guild.roles, id=1229309971641143336)
                    
                    
                    await member2.add_roles(role)
                    await member.add_roles(role)
                    
                    
                    await inter.response.edit_message()
                    
                    embedув = disnake.Embed(color=0x2F3136)
                    server_avatar_url = inter.guild.icon.url if inter.guild.icon else None
                    embedув.set_author(name="Cat | Свадьба", icon_url=server_avatar_url)
                    embedув.add_field(name='⠀', value=f'> Вы успешно заключили брак')
                    embedув.set_thumbnail(url=inter.author.display_avatar.url)
                    
                    
                    await inter.edit_original_message(embed=embedув, view=None)
            else:
                await inter.response.send_message("Ошибка: не удалось найти участников брака.", ephemeral=True)






        elif inter.component.custom_id == "ofcorsenobutton":
            embed = disnake.Embed(color=0x2F3136)
            server_avatar_url = inter.guild.icon.url if inter.guild.icon else None
            embed.set_author(name="Cat | Свадьба", icon_url=server_avatar_url)
            await inter.response.edit_message()
            embed.add_field(name=f'⠀', value=f'> Ну и пошла нахер вумин')
            await self.marry_db.remove_user(inter.author)
            embed.set_thumbnail(url=inter.author.display_avatar.url)
            await inter.edit_original_message(embed=embed, view=None)      





    @commands.Cog.listener()
    async def on_voice_state_update(self, member: disnake.Member, before: disnake.VoiceState, after: disnake.VoiceState):
        
        if after.channel and after.channel.id == 1228353476002582579:
            
            user_data = await self.marry_db.get_user(member)
            if user_data:
                partner_id = user_data[1]
                room_name = user_data[5] if user_data[5] else 'я партнер'
                
                partner = member.guild.get_member(partner_id)
                if partner:
                    category = member.guild.get_channel(1228353273153720493)
                    overwrites = {
                        member.guild.default_role: disnake.PermissionOverwrite(connect=False),
                        member: disnake.PermissionOverwrite(connect=True),
                        partner: disnake.PermissionOverwrite(connect=True)
                    }
                    
                    if room_name != 'я партнер':
                        channel_name = room_name
                    else:
                        channel_name = f"{member.display_name} {room_name} {partner.display_name}"
                    private_channel = await category.create_voice_channel(name=channel_name, overwrites=overwrites)
                    
                    await member.move_to(private_channel)
                    
                    self.temp_channels[private_channel.id] = private_channel

        
        if before.channel and before.channel.id in self.temp_channels:
            
            channel = member.guild.get_channel(before.channel.id)
            
            if channel and len(channel.members) == 0:
                await channel.delete()
                del self.temp_channels[before.channel.id]


def setup(bot):
    bot.add_cog(Marry(bot))          



       
        
