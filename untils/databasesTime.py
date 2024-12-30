import datetime
from datetime import datetime, timedelta
import aiosqlite
import disnake


class CooldownDatabase:
    def __init__(self):
        self.name = 'dbs/cooldowns.db'

    async def create_table(self):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = '''
                CREATE TABLE IF NOT EXISTS cooldowns (
                    user_id INTEGER PRIMARY KEY,
                    last_used  TEXT NOT NULL
                );
                '''
                await cursor.executescript(query)
            await db.commit()

    async def get_cooldown(self, user_id: int):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'SELECT last_used FROM cooldowns WHERE user_id = ?'
                await cursor.execute(query, (user_id,))
                result = await cursor.fetchone()
                return result[0] if result else None

    async def set_cooldown(self, user_id: int, current_time):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'INSERT OR REPLACE INTO cooldowns VALUES (?, ?)'
                await cursor.execute(query, (user_id, current_time))
            await db.commit()

    async def check_cooldown(self, user: disnake.Member):
        last_used = await self.get_cooldown(user)
        if last_used is None:
            return timedelta(0)  
        last_used = datetime.fromisoformat(last_used)
        time_passed = datetime.now() - last_used
        if time_passed > timedelta(hours=12):
            return timedelta(0)
        return timedelta(hours=12) - time_passed        