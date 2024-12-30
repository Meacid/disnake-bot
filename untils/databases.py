# Импортируем необходимые модули.
import datetime
from typing import Optional

import aiosqlite
import disnake


class UsersDataBase:
    def __init__(self, db_path="users.db"):  
        self.db_path = db_path
        self.name = 'dbs/users.db'

    LEVEL_REQUIREMENTS = {
    1: 100,
    2: 300,
    3: 500,
    4: 1000,
    5: 1500,
    6: 2500,
    7: 3500,
    8: 4500  
    }

    
 


    async def create_table(self):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query_users = '''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    money INTEGER,
                    voice_time INTEGER,
                    experience INTEGER,
                    lvl INTEGER, 
                    message_count INTEGER,
                    status TEXT NOT NULL
                    
                );
                '''
                query_transactions = '''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    amount INTEGER NOT NULL,
                    time TEXT NOT NULL,
                    description TEXT NOT NULL
                );
                '''
                await cursor.execute(query_users)
                await cursor.execute(query_transactions)
                await db.commit()

    
    async def get_user(self, user: disnake.Member):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'SELECT * FROM users WHERE id = ?'
                await cursor.execute(query, (user.id,))
                return await cursor.fetchone()

    
    async def add_user(self, user: disnake.Member):
        async with aiosqlite.connect(self.name) as db:
            if not await self.get_user(user):
                async with db.cursor() as cursor:
                    query = 'INSERT INTO users (id, money, voice_time, experience, lvl, message_count, status) VALUES (?, ?, ?, ?, ?, ?, ?)'
                    await cursor.execute(query, (user.id, 0, 0, 0, 0, 0, 'Не установлен'))
                    await db.commit()

    async def update_voice_time(self, user_id, voice_time):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = "UPDATE users SET voice_time = voice_time + ? WHERE id = ?"
                await cursor.execute(query, (voice_time, user_id))
                await db.commit()             

    async def update_experience(self, user: disnake.Member, experience: int):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'UPDATE users SET experience = experience + ? WHERE id = ?'
                await cursor.execute(query, (experience, user.id))
                await db.commit()

    async def update_message_count(self, user: disnake.Member, message_count: int):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'UPDATE users SET message_count = message_count + ? WHERE id = ?'
                await cursor.execute(query, (message_count, user.id))
                await db.commit()            
        
    async def update_money(self, user: disnake.Member, money: int):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'UPDATE users SET money = money + ? WHERE id = ?'
                await cursor.execute(query, (money, user.id))
                await db.commit()

    async def update_experience(self, user: disnake.Member, experience: int):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'UPDATE users SET experience = experience + ? WHERE id = ?'
                await cursor.execute(query, (experience, user.id))
                await db.commit()   

    async def update_status(self, user: disnake.Member, status: str):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'UPDATE users SET status = ? WHERE id = ?'
                await cursor.execute(query, (status, user.id))
                await db.commit()             

                

    async def update_lvl(self, user: disnake.Member, lvl: int):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'UPDATE users SET lvl = lvl + ? WHERE id = ?'
                await cursor.execute(query, (lvl, user.id))
                await db.commit()                      

    async def check_level_up(self, user: disnake.Member):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'SELECT experience, lvl FROM users WHERE id = ?'
                await cursor.execute(query, (user.id,))
                result = await cursor.fetchone()
                if not result:
                    return

                experience, current_lvl = result

                max_achievable_level = current_lvl

                while True:
                    next_lvl = max_achievable_level + 1
                    required_exp = self.LEVEL_REQUIREMENTS.get(next_lvl)

                    if required_exp is None or experience < required_exp:
                        break

                    max_achievable_level = next_lvl

                if max_achievable_level > current_lvl:
                    coins_to_give = 0
                    for level in range(current_lvl + 1, max_achievable_level + 1):
                        coins_to_give += level * 100

                    query = 'SELECT money FROM users WHERE id = ?'
                    await cursor.execute(query, (user.id,))
                    result = await cursor.fetchone()
                    current_money = result[0] if result else 0

                    new_money = current_money + coins_to_give
                    query = 'UPDATE users SET lvl = ?, money = ? WHERE id = ?'
                    await cursor.execute(query, (max_achievable_level, new_money, user.id))

                    await db.commit()


    async def get_top(self):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'SELECT * FROM users ORDER BY money DESC'
                await cursor.execute(query)
                return await cursor.fetchall()

    async def get_top_messages(self):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'SELECT * FROM users ORDER BY message_count DESC'
                await cursor.execute(query)
                return await cursor.fetchall()        

    async def get_top_voice(self):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'SELECT * FROM users ORDER BY voice_time DESC'
                await cursor.execute(query)
                return await cursor.fetchall()

    async def get_voice_position(self, user_id: int) -> int:
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'SELECT id FROM users ORDER BY voice_time DESC'
                await cursor.execute(query)
                results = await cursor.fetchall()
                for position, (id,) in enumerate(results, 1):
                    if id == user_id:
                        return position
                return 0

    async def get_transactions(self, user_id: int):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'SELECT * FROM transactions WHERE user_id = ?'
                await cursor.execute(query, (user_id,))
                return await cursor.fetchall()

    
    async def add_transaction(self, user_id: int, amount: int, description: str):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                current_time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
                query = 'INSERT INTO transactions (user_id, amount, time, description) VALUES (?, ?, ?, ?)'
                await cursor.execute(query, (user_id, amount, current_time, description))
                await db.commit()

    
    async def get_embeds(self, interaction, top_type="balance"):
        if top_type == "balance":
            data = await self.get_top()  
            title = "Топ пользователей по балансу"
        elif top_type == "messages":
            data = await self.get_top_messages()  
            title = "Топ пользователей по сообщениям"
        elif top_type == "voice":
            data = await self.get_top_voice()  
            title = "Топ пользователей по времени в голосовых каналах"
        else:
            return []  

        embeds = []
        n = 0
        loop_count = 0
        text = ""
        for row in data:
            n += 1
            
            loop_count += 1
            if loop_count % 10 == 0 or loop_count - 1 == len(data) - 1:
                embed = disnake.Embed(title=title, description=text, color=0x2F3136)
                embeds.append(embed)
                text = ""
        return embeds

    async def get_transaction_embeds(self, interaction):
        transactions = await self.get_transactions(interaction.author.id)
        if not transactions:
            return []
        
        embeds = []
        transactions_per_page = 5
        
        for i in range(0, len(transactions), transactions_per_page):
            embed = disnake.Embed(title="История транзакций", color=0x2F3136)
            embed.set_author(name=interaction.author.display_name, icon_url=interaction.author.display_avatar)
            
            page_transactions = transactions[i:i + transactions_per_page]
            for trans in page_transactions:
                _, _, amount, time, description = trans
                sign = '+' if amount > 0 else ''
                embed.add_field(
                    name=f"{'🟢' if amount > 0 else '🔴'} {time}",
                    value=f"```{sign}{amount} 💰\n{description}```",
                    inline=False
                )
            
            embeds.append(embed)
        
        return embeds
