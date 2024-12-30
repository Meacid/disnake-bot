import disnake
from disnake.ext import commands
from untils.databases import UsersDataBase
import os
class PaginatorView(disnake.ui.View):
    def __init__(self, embeds, author, footer: bool, timeout=30.0):
        self.embeds = embeds
        self.author = author
        self.footer = footer
        self.timeout = timeout
        self.page = 0  
        super().__init__(timeout=self.timeout)

        if self.footer:
            for emb in self.embeds:
                emb.set_footer(text=f'Страница {self.embeds.index(emb) + 1} из {len(self.embeds)}')




    @disnake.ui.button(label='◀️', style=disnake.ButtonStyle.grey)
    async def back(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        if self.author.id == interaction.author.id:
            if self.page == 0:
                self.page = len(self.embeds) - 1
            else:
                self.page -= 1
        else:
            return

        await self.button_callback(interaction)

    @disnake.ui.button(label='▶️', style=disnake.ButtonStyle.grey)
    async def next(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        if self.author.id == interaction.author.id:
            if self.page == len(self.embeds) - 1:
                self.page = 0
            else:
                self.page += 1
        else:
            return

        await self.button_callback(interaction)

    async def button_callback(self, interaction):
        if self.author.id == interaction.author.id:
            await interaction.response.edit_message(embed=self.embeds[self.page])
        else:
            return await interaction.response.send_message('Вы не можете использовать эту кнопку!', ephemeral=True)

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = UsersDataBase()

    @commands.slash_command(name='balance', description='Посмотреть баланс пользователя')
    async def balance(self, interaction, member: disnake.Member = (commands.Param(description='Выберите юзера', default=None))):
        await self.db.create_table()  
        if not member:
            member = interaction.author  
        await self.db.add_user(member)  
        user = await self.db.get_user(member)  
        embed = disnake.Embed(color=0x2F3136)
        embed.add_field(name=f'Текущий баланс - {member}', value=f' ```{user[1]}```')  
        embed.set_thumbnail(url=member.display_avatar.url)  

        await interaction.response.send_message(embed=embed)

    @commands.slash_command(name='transfer', description='Зробити передачу валюти іншому юзеру')
    async def transfer(self, interaction, member: disnake.Member = (commands.Param(description='Треба вибрати юзера')), amount: int = commands.Param(description='Треба вибрати кількість', gt=50, le=10000)):  
        await self.db.create_table() 
        await self.db.add_user(member)
        await self.db.add_transaction(interaction.author.id, amount, f"Передав {interaction.author}")  # Добавляем пользователя в базу данных, если его там нет.

        await self.db.update_money(member, amount)
        await self.db.update_money(interaction.author, -amount)

        embed = disnake.Embed(color=0x2F3136)
        server_avatar_url = interaction.guild.icon.url if interaction.guild.icon else None
        embed.set_author(name="Cat | Transfer", icon_url=server_avatar_url)
        embed.description = f'{interaction.author.mention} передав {member.mention} {amount} .'
        embed.set_thumbnail(url=member.display_avatar.url)
        await interaction.response.send_message(embed=embed)


    @commands.slash_command(name='gift', description='Збільшити баланс юзеру')
    @commands.has_permissions(administrator=True)
    async def gift(self, interaction, member: disnake.Member = (commands.Param(description='Треба вибрати юзера')), amount: int = commands.Param(description='Треба вибрати кількість', gt=-1000000, le=1000000)):  
        await self.db.create_table()  
        await self.db.add_user(member)
        await self.db.add_transaction(member.id, amount,"Видав Адміністратор")  

        await self.db.update_money(member, amount)  

        embed = disnake.Embed(color=0x2F3136)
        server_avatar_url = interaction.guild.icon.url if interaction.guild.icon else None
        embed.set_author(name="Cat | Gift", icon_url=server_avatar_url)
        embed.description = f'{interaction.author.mention} видав {member.mention} {amount} .'
        embed.set_thumbnail(url=member.display_avatar.url)  

        await interaction.response.send_message(embed=embed)    


    @commands.slash_command(name='add_exp', description='Збільшити exp юзеру')
    async def add_exp(self, interaction, member: disnake.Member = (commands.Param(description='Треба вибрати юзера')), amount: int = commands.Param(description='Треба вибрати кількість')):  
        await self.db.create_table()  
        await self.db.add_user(member) 

        await self.db.update_experience(member, amount)  

        embed = disnake.Embed(color=0x2F3136)
        server_avatar_url = interaction.guild.icon.url if interaction.guild.icon else None
        embed.set_author(name="Cat | add_exp", icon_url=server_avatar_url)
        embed.description = f'Администратор {interaction.author.mention} видав {member.mention} {amount} опыта .'
        embed.set_thumbnail(url=member.display_avatar.url)  
        await self.db.check_level_up(interaction.author)

        await interaction.response.send_message(embed=embed, ephemeral = True )   


    @commands.slash_command(name='add_lvl', description='Збільшити lvl юзеру')
    @commands.has_permissions(administrator=True)
    async def addlvl(self, interaction, member: disnake.Member = (commands.Param(description='Треба вибрати юзера')), amount: int = commands.Param(description='Треба вибрати кількість')):  
        await self.db.create_table()  
        await self.db.add_user(member) 

        await self.db.update_lvl(member, amount)  

        embed = disnake.Embed(color=0x2F3136)
        server_avatar_url = interaction.guild.icon.url if interaction.guild.icon else None
        embed.set_author(name="Cat | add_lvl", icon_url=server_avatar_url)
        embed.description = f'Администратор {interaction.author.mention} видав {member.mention} {amount} lvl .'
        embed.set_thumbnail(url=member.display_avatar.url)  
        await self.db.check_level_up(interaction.author)

        await interaction.response.send_message(embed=embed, ephemeral = True )       


    @commands.slash_command(name='set', description='Змінити баланс юзеру')
    @commands.has_permissions(administrator=True)
    async def set(self, interaction, member: disnake.Member = (commands.Param(description='Треба вибрати юзера')), amount: int = commands.Param(description='Треба вибрати кількість', gt=-1000000, le=1000000)):  
        await self.db.create_table()  
        await self.db.add_user(member)  
        user_data = await self.db.get_user(member)
        current_money = user_data[1]  
        await self.db.update_money(member, amount - current_money)
          

        embed = disnake.Embed(color=0x2F3136)
        server_avatar_url = interaction.guild.icon.url if interaction.guild.icon else None
        embed.set_author(name="Cat | Set", icon_url=server_avatar_url)
        embed.description = f'{interaction.author.mention} змінив баланс {member.mention} на {amount} .'
        embed.set_thumbnail(url=member.display_avatar.url)  

        await interaction.response.send_message(embed=embed) 


    @commands.slash_command(name='top', description='Посмотреть топ пользователей')
    async def top(self, interaction):
        await self.db.create_table()
        top = await self.db.get_top()
        embeds = []
        loop_count = 0
        n = 0
        text = ''
        for user in top:
            n += 1
            loop_count += 1
            text += f'**{n}.** <@{user[0]}> - {user[1]} :coin:\n' 
            if loop_count % 10 == 0 or loop_count - 1 == len(top) - 1:
                embed = disnake.Embed(color=0x2F3136, title='Топ 10 по балансу')
                embed.description = text
                embed.set_thumbnail(url=interaction.author.display_avatar.url)
                embeds.append(embed)
                text = ''

        view = disnake.ui.View()
        select_menu = SelectGames()
        view.add_item(select_menu) 
        

        await interaction.response.send_message(embed=embeds[0], view=view)





    
       



class SelectGames(disnake.ui.Select):
    def __init__(self):
        self.db = UsersDataBase()
        options = [
            disnake.SelectOption(
                label="Топ по балансу"
                
            ),
            disnake.SelectOption(
                label="Топ по онлайну"
                
            ),
            disnake.SelectOption(
                label="Топ по сообщениям",
            )
        ]
        super().__init__(placeholder="Укажите топ", options=options, custom_id="top", min_values=0, max_values=1)

    async def top(self, interaction):
        await self.db.create_table()

        top = await self.db.get_top()
        embeds = []
        loop_count = 0
        n = 0
        text = ''
        for user in top:
            n += 1
            loop_count += 1
            text += f'**{n}.** <@{user[0]}> - {user[1]} :coin:\n' 
            if loop_count % 10 == 0 or loop_count - 1 == len(top) - 1:
                embed = disnake.Embed(color=0x2F3136, title='Топ 10 по балансу')
                embed.description = text
                embed.set_thumbnail(url=interaction.author.display_avatar.url)
                embeds.append(embed)
                text = ''
                
        view = disnake.ui.View()
        view.add_item(SelectGames()) 
        await interaction.edit_original_response(embed=embeds[0], view=view)    

    async def top_messages(self, interaction):
        await self.db.create_table() 
        top = await self.db.get_top_messages() 
        embeds = []
        loop_count = 0
        n = 0
        text = ''
        for user in top:
            n += 1
            loop_count += 1
            text += f'**{n}.** <@{user[0]}> - {user[5]} сообщений\n' 
            if loop_count % 10 == 0 or loop_count - 1 == len(top) - 1:
                embed = disnake.Embed(color=0x2F3136, title='Топ 10 по сообщениям')
                embed.description = text
                embed.set_thumbnail(url=interaction.author.display_avatar.url)
                embeds.append(embed)
                text = ''
        view = disnake.ui.View()
        view.add_item(SelectGames())
        await interaction.edit_original_response(embed=embeds[0], view=view)   

    async def top_online(self, interaction):
        await self.db.create_table()
        top = await self.db.get_top_messages()

        
        top.sort(key=lambda user: user[2], reverse=True)

        embeds = []
        text = ''
        loop_count = 0

        for n, user in enumerate(top, start=1):
            loop_count += 1
            seconds = user[2]
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60

            text += f"**{n}.** <@{user[0]}> - онлайн: {hours} ч. {minutes} мин.\n"

            if loop_count % 10 == 0 or loop_count == len(top):
                embed = disnake.Embed(color=0x2F3136, title='Топ 10 по онлайну')
                embed.description = text
                embed.set_thumbnail(url=interaction.author.display_avatar.url)
                embeds.append(embed)
                text = ''

        view = disnake.ui.View()
        view.add_item(SelectGames())
        await interaction.edit_original_response(embed=embeds[0], view=view)    

    
    async def callback(self, interaction: disnake.MessageInteraction):
        await interaction.response.defer()

        selected_values = self.values  

        if "Топ по балансу" in selected_values:
            await self.top(interaction)
        elif "Топ по сообщениям" in selected_values:
            await self.top_messages(interaction)
        elif "Топ по онлайну" in selected_values:
            await self.top_online(interaction)
                

def setup(bot):
    bot.add_cog(Economy(bot))
