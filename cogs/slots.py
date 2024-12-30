import disnake
from disnake.ext import commands
import random
from untils.databases import UsersDataBase

class Slots(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = UsersDataBase()

    @commands.slash_command(name='slots', description='Игра в слоты')
    @commands.cooldown(1,30, commands.BucketType.user)
    async def slots(self, interaction, ставка: int = commands.Param(description='Выберите сумму', gt=50, le=10000)):
        await self.db.create_table()
        member = interaction.author
        await self.db.add_user(member)

        user = await self.db.get_user(member)
        if user[1] < ставка:
            embed = disnake.Embed(color=0x2F3136)
            embed.description = f'{interaction.author.mention} у вас недостаточно монет для ставки.'
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        fruits = ['🍇', '🍊', '🍋', '🍉', '🍌']

        
        slot_results = [random.choice(fruits) for _ in range(3)]
        result_str = ' | '.join(slot_results)

        
        if len(set(slot_results)) == 1:
            
            boost = f'x{random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])}'
            won_amount = ставка * int(boost[1:])
            embed_description = f'> {interaction.author.mention}, вы **выиграли**, на ваш баланс зачислено **{won_amount}**\n> Ваш множитель: **{boost}**'
            await self.db.update_money(member, won_amount)
            await self.db.add_transaction(interaction.author.id, won_amount,"Выигрыш в слотах")
        elif len(set(slot_results)) == 2:
            
            boost = 'x1'
            won_amount = ставка * int(boost[1:])
            embed_description = f'> {interaction.author.mention}, вы **выиграли**, на ваш баланс зачислено **{won_amount}**\n> Ваш множитель: **{boost}**'
            await self.db.update_money(member, won_amount)
            await self.db.add_transaction(interaction.author.id, won_amount,"Выигрыш в слотах")
        else:
            
            embed_description = f'> {interaction.author.mention}, вы програли: **{ставка}**'
            await self.db.add_transaction(interaction.author.id, -ставка,"Проигрыш в слотах")
            await self.db.update_money(member, -ставка)

        embed = disnake.Embed()
        server_avatar_url = interaction.guild.icon.url if interaction.guild.icon else None
        embed.set_author(name="Cat | Слоты", icon_url=server_avatar_url)
        embed.set_thumbnail(url=interaction.author.display_avatar.url)
        embed.add_field(name=f'``` {result_str} ```', value="⠀", inline=False)
        embed.description = embed_description
        await interaction.response.send_message(embed=embed)
        
    @slots.error  
    async def slots_error(self, inter, error):
        member = inter.author
        if isinstance(error, commands.CommandOnCooldown):
            seconds_left = error.retry_after
            embed = disnake.Embed(color=0x2F3136)
            server_avatar_url = inter.guild.icon.url if inter.guild.icon else None
            embed.set_author(name="Cat | Slots", icon_url=server_avatar_url)
            embed.set_thumbnail(url=inter.author.display_avatar.url)
            embed.add_field(name=f'', value=f'> {member.mention}, вы слишком часто используете команду, приходите через **{seconds_left:.2f}** секунд')
            embed.set_thumbnail(url=member.display_avatar.url)
            await inter.response.send_message(embed=embed, ephemeral = True)    

def setup(bot):
    bot.add_cog(Slots(bot))
