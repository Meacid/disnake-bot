from typing import Optional
import disnake
from disnake.ext import commands
import random
from untils.databases import UsersDataBase
import asyncio

emoji = "<:hrtfk:1216062579600789644>"


class Coinflip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = UsersDataBase()
        self.lock = asyncio.Lock()  

    @commands.slash_command(name='coinflip', description='Коінфліп')
    async def coinflip(self, inter, сумма: int = commands.Param(description='Виберіть кількість монет', gt=50, le=50000)):
        await self.db.create_table()
        member = inter.author  
        await self.db.add_user(member)

        user = await self.db.get_user(member)
        embed = disnake.Embed(color=0x2F3136)

        if user[1] < сумма:
            embed.description = f'{inter.author.mention} у вас недостатньо коштів для здійснення операції.'
            await inter.response.send_message(embed=embed, ephemeral=True)
            return

        coin_buttons = [
            disnake.ui.Button(style=disnake.ButtonStyle.gray, label="Орел", custom_id="coinflip_or"),
            disnake.ui.Button(style=disnake.ButtonStyle.gray, label="Решка", custom_id="coinflip_reshka")
        ]
        coin_view = disnake.ui.View()
        for button in coin_buttons:
            coin_view.add_item(button)

        server_avatar_url = inter.guild.icon.url if inter.guild.icon else None
        embed.set_author(name='Cat | Коінфліп', icon_url=server_avatar_url)
        embed.description = f'{inter.author.mention} виберіть сторону'
        embed.set_thumbnail(url=member.display_avatar.url)
        await inter.response.send_message(embed=embed, view=coin_view)

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        async with self.lock:  
            if inter.component.custom_id in ["coinflip_or", "coinflip_reshka"]:
                
                original_message = await inter.original_message()
                try:
                    mentioned_user_id = int(original_message.embeds[0].description.split(" ")[0][2:-1])
                except (IndexError, ValueError):
                    return  

                if inter.author.id != mentioned_user_id:
                    await inter.response.send_message("Ви не можете грати в цю гру.", ephemeral=True)
                    return

                сторона = inter.component.label

                await inter.response.defer() 

                gif_embed = disnake.Embed(color=0x2F3136)
                gif_embed.set_image(url="https://media.tenor.com/-Ty-f7Ld7skAAAAC/anime-coinflip.gif")

                await inter.edit_original_message(embed=gif_embed, view=None)

                await asyncio.sleep(5)

                bot_choice = random.choice(["Орел", "Решка"])  
                result_embed = disnake.Embed(color=0x2F3136)

                if сторона == bot_choice:
                    field_value = f'Ви **виграли**, на ваш баланс зараховано **{self.сумма}** {emoji}\n'
                    await self.db.update_money(inter.author, self.сумма)  # Используйте inter.author
                    await self.db.add_transaction(inter.author.id, self.сумма, "Виграш у коінфліп")
                else:
                    field_value = f'Ви програли: **{self.сумма}** {emoji}\n '
                    await self.db.update_money(inter.author, -self.сумма)  
                    await self.db.add_transaction(inter.author.id, -self.сумма, "Проіграш в коінфліп")

                server_avatar_url = inter.guild.icon.url if inter.guild.icon else None
                result_embed.set_author(name='Cat | Коінфліп', icon_url=server_avatar_url)
                result_embed.add_field(name=field_value, value='⠀', inline=False)
                result_embed.set_thumbnail(url=inter.author.display_avatar.url)

                await inter.edit_original_message(embed=result_embed, view=None)


def setup(bot):
    bot.add_cog(Coinflip(bot))
