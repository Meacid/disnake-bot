import datetime
import aiosqlite
import disnake
emoji = "<:moon:1157277204670058526>"


class MarryDatabase:
    def __init__(self):
        self.name = 'dbs/marry.db'  

    async def create_table(self):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = '''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    partner_id INTEGER,
                    voice_time INTEGER,
                    marriage_date TEXT NOT NULL,
                    image TEXT,
                    name TEXT
                );
                '''
                await cursor.executescript(query)
            await db.commit()


    async def update_voice_time(self, user_id, time):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'UPDATE users SET voice_time = voice_time + ? WHERE id = ?'
                await cursor.execute(query, (time, user_id))
                await db.commit()     

    async def update_name(self, user_id, room_name):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'UPDATE users SET name = ? WHERE id = ?'
                await cursor.execute(query, (room_name, user_id))
                await db.commit()                 

    async def get_user(self, user: disnake.Member):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'SELECT * FROM users WHERE id = ? OR partner_id = ?'
                await cursor.execute(query, (user.id, user.id))
                return await cursor.fetchone()    

    async def add_user(self, user1: disnake.Member, user2: disnake.Member, marriage_date):
        async with aiosqlite.connect(self.name) as db:
            if not await self.get_user(user1):
                async with db.cursor() as cursor: 
                    query = 'INSERT INTO users (id, partner_id, voice_time, marriage_date, image, name) VALUES (?, ?, ?, ?, ?, ?)'
                    await cursor.execute(query, (user1.id, user2.id, 0, marriage_date, None, '❤️'))  
                    await db.commit()    
                                

                     
               


    async def remove_user(self, user: disnake.Member):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'DELETE FROM users WHERE id = ? OR partner_id = ?'
                await cursor.execute(query, (user.id, user.id))
                await db.commit()                 

    async def update_user_image(self, user: disnake.Member, image_url: str):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'UPDATE users SET image = ? WHERE id = ?'
                await cursor.execute(query, (image_url, user.id))
                await db.commit()

    async def delete_banner(self, user_id):
        async with aiosqlite.connect(self.name) as db:
            async with db.cursor() as cursor:
                query = 'UPDATE users SET image = NULL WHERE id = ?'
                await cursor.execute(query, (user_id,))
                await db.commit()

    def format_date(self, date_str: str) -> str:
        try:
            date = datetime.datetime.fromisoformat(date_str)
            return date.strftime('%d.%m.%Y')
        except:
            return date_str