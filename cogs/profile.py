import io
import asyncio
import datetime
from datetime import datetime
import aiohttp
import disnake
from disnake.ext import commands
from PIL import Image, ImageFont, ImageDraw

from untils.databases import UsersDataBase
from untils.databasesMarry import MarryDatabase

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = UsersDataBase()
        self.marry_db = MarryDatabase()

    async def get_avatar(self, url: str) -> bytes:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                avatar = await resp.read()
        return avatar

    async def limit_string_length(self, string, max_length=15):
        return f'{string[:max_length-1]}...' if len(string) > max_length else string

    class AddBannerModal(disnake.ui.Modal):
        def __init__(self, bot, member):
            components = [
                disnake.ui.TextInput(label='URL изображения', custom_id='image_url', style=disnake.TextInputStyle.short)
            ]
            super().__init__(title='Добавить баннер', components=components)
            self.bot = bot
            self.member = member

        async def resize_image(self, url: str) -> str:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status != 200:
                            return url
                        
                        image_data = await response.read()
                        image = Image.open(io.BytesIO(image_data))
                        
                        
                        max_size = (400, 200)  
                        image.thumbnail(max_size, Image.Resampling.LANCZOS)
                        
                        
                        buffer = io.BytesIO()
                        image.save(buffer, format='PNG')
                        buffer.seek(0)
                        
                        
                        file = disnake.File(buffer, filename='banner.png')
                        message = await self.bot.get_channel(YOUR_CHANNEL_ID).send(file=file)  # Замените YOUR_CHANNEL_ID на ID канала для хранения
                        return message.attachments[0].url
            except:
                return url

        async def check_image(self, url: str) -> tuple[bool, str]:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status != 200:
                            return False, "Не удалось загрузить изображение"
                        
                        if int(response.headers.get('Content-Length', 0)) > 2 * 1024 * 1024:
                            return False, "Размер изображения не должен превышать 2MB"
                        
                        content_type = response.headers.get('Content-Type', '')
                        if not content_type.startswith('image/'):
                            return False, "URL должен вести на изображение"
                        
                        return True, "OK"
            except:
                return False, "Неверный URL изображения"

        async def callback(self, interaction: disnake.ModalInteraction):
            image_url = interaction.text_values['image_url']
            
            is_valid, message = await self.check_image(image_url)
            if not is_valid:
                await interaction.response.send_message(message, ephemeral=True)
                return
            
            
            await interaction.response.defer(ephemeral=True)
            resized_url = await self.resize_image(image_url)
            
            marry_db = MarryDatabase()
            await marry_db.update_user_image(self.member, resized_url)
            await interaction.followup.send('Баннер обновлён!', ephemeral=True)

    class ChangeRoomNameModal(disnake.ui.Modal):
        def __init__(self, bot, member):
            components = [
                disnake.ui.TextInput(label='Новое название комнаты', custom_id='room_name', style=disnake.TextInputStyle.short)
            ]
            super().__init__(title='Изменить название комнаты', components=components)
            self.bot = bot
            self.member = member

        async def callback(self, interaction: disnake.ModalInteraction):
            room_name = interaction.text_values['room_name']
            marry_db = MarryDatabase()
            await marry_db.update_name(self.member.id, room_name)
            await interaction.response.send_message('Название комнаты обновлено!', ephemeral=True)

    class LoveProfileButton(disnake.ui.Button):
        def __init__(self, bot, member):
            super().__init__(style=disnake.ButtonStyle.blurple, label='Любовный профиль')
            self.bot = bot
            self.member = member

        async def callback(self, interaction: disnake.Interaction):
            marry_db = MarryDatabase()
            user = await marry_db.get_user(self.member)
            if not user:
                await interaction.response.send_message('У вас нет любовного профиля!', ephemeral=True)
                return

            partner = self.bot.get_user(user[1])
            if not partner:
                partner = await self.bot.fetch_user(user[1])

            voice_hours = user[2] // 3600
            voice_minutes = (user[2] % 3600) // 60
            marriage_date = marry_db.format_date(user[3])
            room_name = user[5] if user[5] else "Не установлено"
            
            
            db = UsersDataBase()
            user_data = await db.get_user(self.member)
            status = user_data[2] if user_data and user_data[2] else "Не установлен"

            embed = disnake.Embed(title=f"**Любовный Профиль - {self.member.display_name}**", color=0x2F3136)
            embed.add_field(name="> Партнер", value=f"```{partner.name}```", inline=True)
            embed.add_field(name="> Дата свадьбы", value=f"```{marriage_date} ```", inline=True)
            embed.add_field(name="> Название комнаты", value=f"```{room_name}```", inline=True)
            embed.add_field(name="> Совместный онлайн", value=f"```{voice_hours}ч, {voice_minutes}м   ```", inline=True)
            embed.set_thumbnail(url=self.member.display_avatar.url)

            if user[4]:  
                embed.set_image(url=user[4])

            view = disnake.ui.View()
            view.add_item(Profile.AddBannerButton(self.bot, self.member))
            view.add_item(Profile.DeleteBannerButton(self.bot, self.member))
            view.add_item(Profile.ChangeRoomNameButton(self.bot, self.member))
            view.add_item(Profile.BackToProfileButton(self.bot, self.member))

            await interaction.response.edit_message(embed=embed, view=view)

    class AddBannerButton(disnake.ui.Button):
        def __init__(self, bot, member):
            super().__init__(style=disnake.ButtonStyle.green, label='Добавить баннер')
            self.bot = bot
            self.member = member

        async def callback(self, interaction: disnake.Interaction):
            await interaction.response.send_modal(Profile.AddBannerModal(self.bot, self.member))

    class DeleteBannerButton(disnake.ui.Button):
        def __init__(self, bot, member):
            super().__init__(style=disnake.ButtonStyle.red, label='Удалить баннер')
            self.bot = bot
            self.member = member

        async def callback(self, interaction: disnake.Interaction):
            if interaction.user.id != self.member.id:
                await interaction.response.send_message('Вы можете удалить только свой баннер!', ephemeral=True)
                return
            
            marry_db = MarryDatabase()
            user = await marry_db.get_user(self.member)
            if not user or not user[4]:  
                await interaction.response.send_message('У вас нет установленного баннера!', ephemeral=True)
                return
                
            await marry_db.delete_banner(self.member.id)
            await interaction.response.send_message('Баннер успешно удален!', ephemeral=True)

    class ChangeRoomNameButton(disnake.ui.Button):
        def __init__(self, bot, member):
            super().__init__(style=disnake.ButtonStyle.green, label='Изменить название комнаты')
            self.bot = bot
            self.member = member

        async def callback(self, interaction: disnake.Interaction):
            modal = Profile.ChangeRoomNameModal(self.bot, self.member)
            await interaction.response.send_modal(modal)

    class ChangeStatusModal(disnake.ui.Modal):
        def __init__(self, bot, member):
            components = [
                disnake.ui.TextInput(
                    label='Новый статус',
                    custom_id='status',
                    style=disnake.TextInputStyle.paragraph,
                    max_length=30,
                    placeholder='Введите ваш новый статус'
                )
            ]
            super().__init__(title='Изменить статус', components=components)
            self.bot = bot
            self.member = member

        async def callback(self, interaction: disnake.ModalInteraction):
            new_status = interaction.text_values['status']
            db = UsersDataBase()
            await db.update_status(self.member, new_status)
            await interaction.response.send_message('Статус обновлён!', ephemeral=True)

    class ChangeStatusButton(disnake.ui.Button):
        def __init__(self, bot, member):
            super().__init__(style=disnake.ButtonStyle.green, label='Изменить статус')
            self.bot = bot
            self.member = member

        async def callback(self, interaction: disnake.Interaction):
            if interaction.user.id != self.member.id:
                await interaction.response.send_message('Вы можете изменить только свой статус!', ephemeral=True)
                return
            modal = Profile.ChangeStatusModal(self.bot, self.member)
            await interaction.response.send_modal(modal)

    class BackToProfileButton(disnake.ui.Button):
        def __init__(self, bot, member):
            super().__init__(style=disnake.ButtonStyle.gray, label='Вернуться к профилю')
            self.bot = bot
            self.member = member
            self.db = UsersDataBase()
            self.marry_db = MarryDatabase()

        async def callback(self, interaction: disnake.Interaction):
            await self.db.create_table()
            await self.marry_db.create_table()
            await self.db.add_user(self.member)
            user = await self.db.get_user(self.member)
            
            status = str(user[6]) if user[6] is not None else "Не установлен"
            level = str(user[4]) if user[4] is not None else "0"
            coins = str(user[1]) if user[1] is not None else "0"
            
            hours = user[2] // 3600
            minutes = (user[2] % 3600) // 60
            
            embed = disnake.Embed(title=f"**Профиль - {self.member.display_name}**", color=0x2F3136)
            embed.add_field(name="> Статус", value=f"```{status}   ```", inline=False)
            embed.add_field(name="> Уровень", value=f"```{level}   ```", inline=True)
            embed.add_field(name="> Коин", value=f"```{coins}   ```", inline=True)
            embed.add_field(name="> Голосовой онлайн", value=f"```{hours}ч, {minutes}м   ```", inline=True)
            embed.set_thumbnail(url=self.member.display_avatar.url)

            view = Profile.ProfileView(self.bot, self.member)
            await interaction.response.edit_message(embed=embed, view=view)

    class ProfileView(disnake.ui.View):
        def __init__(self, bot, member):
            super().__init__()
            self.add_item(Profile.LoveProfileButton(bot, member))
            self.add_item(Profile.ChangeStatusButton(bot, member))

    @commands.slash_command(description='Информация о профиле')
    async def profile(self, inter: disnake.AppCommandInter,
                        member: disnake.Member = commands.Param(default=lambda m: m.author, description='Пользователь')):

        await self.db.create_table()
        await self.marry_db.create_table()
        await self.db.add_user(member)
        user = await self.db.get_user(member)
        
        
        status = str(user[6]) if user[6] is not None else "Не установлен"
        level = str(user[4]) if user[4] is not None else "0"
        coins = str(user[1]) if user[1] is not None else "0"
        
        hours = user[2] // 3600
        minutes = (user[2] % 3600) // 60
        
        embed = disnake.Embed(title=f"**Профиль - {member.display_name}**", color=0x2F3136)
        embed.add_field(name="> Статус", value=f"```{status}   ```", inline=False)
        embed.add_field(name="> Уровень", value=f"```{level}   ```", inline=True)
        embed.add_field(name="> Коин", value=f"```{coins}   ```", inline=True)
        embed.add_field(name="> Голосовой онлайн", value=f"```{hours}ч, {minutes}м   ```", inline=True)
        embed.set_thumbnail(url=member.display_avatar.url)

        view = Profile.ProfileView(self.bot, member)
        await inter.response.send_message(embed=embed, view=view)  
        
        

        
        
        


        
       
        
           

def setup(bot):
    bot.add_cog(Profile(bot))
