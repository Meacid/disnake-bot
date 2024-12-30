import disnake
from disnake.ext import commands
import random
import asyncio
from untils.databases import UsersDataBase



class Roulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = UsersDataBase()
        self.colors = {
            'красный': {'emoji': '🔴', 'multiplier': 2, 'chance': 0.45, 'numbers': [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]},
            'черный': {'emoji': '⚫', 'multiplier': 2, 'chance': 0.45, 'numbers': [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]},
            'зеленый': {'emoji': '🟢', 'multiplier': 15, 'chance': 0.15, 'numbers': [0]}
        }
        self.streak_multipliers = {
            2: 1.2,  
            3: 1.5,  
            4: 2.0, 
            5: 3.0   
        }
        self.user_streaks = {}

    @commands.slash_command(name='roulette', description='Игра в рулетку')
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def roulette(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        ставка: int = commands.Param(description='Выберите сумму', gt=50, le=10000),
        цвет: str = commands.Param(
            description='Выберите цвет (красный ×2, черный ×2, зеленый ×14)',
            choices=['красный', 'черный', 'зеленый']
        )
    ):
        await self.db.create_table()
        member = interaction.author
        await self.db.add_user(member)

        user = await self.db.get_user(member)
        if user[1] < ставка:
            embed = disnake.Embed(color=0x2F3136)
            embed.description = f'{interaction.author.mention} у вас недостаточно монет для ставки.'
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        
        embed = disnake.Embed(color=0x2F3136)
        server_avatar_url = interaction.guild.icon.url if interaction.guild.icon else None
        embed.set_author(name="Cat | Рулетка", icon_url=server_avatar_url)
        embed.set_thumbnail(url=interaction.author.display_avatar.url)

        
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_message()

        
        for _ in range(3):
            number = random.randint(0, 36)
            color = next(color for color, data in self.colors.items() if number in data['numbers'])
            spinning_display = f"{self.colors[color]['emoji']} {number}"
            
            embed.clear_fields()
            embed.add_field(
                name="Рулетка крутится...",
                value=f'```{spinning_display}```',
                inline=False
            )
            await message.edit(embed=embed)
            await asyncio.sleep(0.7)

        
        result = random.random()
        if result < self.colors['зеленый']['chance']:
            winning_color = 'зеленый'
            winning_number = 0
        elif result < self.colors['зеленый']['chance'] + self.colors['красный']['chance']:
            winning_color = 'красный'
            winning_number = random.choice(self.colors['красный']['numbers'])
        else:
            winning_color = 'черный'
            winning_number = random.choice(self.colors['черный']['numbers'])

        
        if winning_color == цвет:
            
            if member.id not in self.user_streaks:
                self.user_streaks[member.id] = 1
            else:
                self.user_streaks[member.id] += 1

            
            streak = self.user_streaks[member.id]
            streak_multiplier = self.streak_multipliers.get(streak, 1.0)
            
            base_amount = ставка * self.colors[цвет]['multiplier']
            won_amount = int(base_amount * streak_multiplier)
            
            streak_bonus = f"\n> Серия побед: **{streak}**\n> Бонус за серию: **x{streak_multiplier}**" if streak > 1 else ""
            embed_description = f'> {interaction.author.mention}, вы **выиграли**!\n> Выпало: {self.colors[winning_color]["emoji"]} **{winning_number}**\n> Ваш выигрыш: **{won_amount}**{streak_bonus}'
            
            await self.db.update_money(member, won_amount)
            await self.db.add_transaction(interaction.author.id, won_amount, "Выигрыш в рулетке")
        else:
            
            self.user_streaks[member.id] = 0
            embed_description = f'> {interaction.author.mention}, вы **проиграли**!\n> Выпало: {self.colors[winning_color]["emoji"]} **{winning_number}**\n> Потеряно: **{ставка}**'
            await self.db.update_money(member, -ставка)
            await self.db.add_transaction(interaction.author.id, -ставка, "Проигрыш в рулетке")

        
        embed.description = embed_description
        embed.clear_fields()
        embed.add_field(
            name="Результат",
            value=f'```Ваша ставка: {ставка}\nВаш цвет: {self.colors[цвет]["emoji"]}\nВыпало: {self.colors[winning_color]["emoji"]} {winning_number}```',
            inline=False
        )

        await message.edit(embed=embed)

    @roulette.error
    async def roulette_error(self, inter, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = disnake.Embed(color=0x2F3136)
            server_avatar_url = inter.guild.icon.url if inter.guild.icon else None
            embed.set_author(name="Cat | Рулетка", icon_url=server_avatar_url)
            embed.set_thumbnail(url=inter.author.display_avatar.url)
            embed.add_field(
                name='',
                value=f'> {inter.author.mention}, подождите **{error.retry_after:.2f}** секунд перед следующей игрой'
            )
            await inter.response.send_message(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Roulette(bot))
