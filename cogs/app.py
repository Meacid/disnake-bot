import asyncio
import disnake
import os
import time
from disnake.ext import commands
import google.generativeai as genai
from config import API_KEY

genai.configure(api_key=API_KEY)

class App(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash-8b',
            system_instruction=f"Ты чат бот.Отвечай в пределах 4 тысячи символов"
                 
        )
        
        self.chats = {}
      
        

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author == self.bot.user:
            return
        if self.bot.user.mentioned_in(message):
            question = message.content.replace(f'<@{self.bot.user.id}>', '').strip()
            if question:
                async with message.channel.typing():
                    try:
                        if message.attachments:
                            for attachment in message.attachments:
                                filename = f"temp.{attachment.filename.split('.')[-1]}"
                                await attachment.save(filename)

                                if attachment.filename.endswith(".pdf"):
                                    sample_pdf = genai.upload_file(filename, mime_type="application/pdf")
                                    if message.author.id not in self.chats:
                                        self.chats[message.author.id] = self.model.start_chat()
                                    chat = self.chats[message.author.id]
                                    response = chat.send_message([question, sample_pdf])
                                    await message.reply(response.text)

                                elif attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                                    sample_image = genai.upload_file(filename, mime_type="image/jpeg")  
                                    if message.author.id not in self.chats:
                                        self.chats[message.author.id] = self.model.start_chat()
                                    chat = self.chats[message.author.id]
                                    response = chat.send_message([question, sample_image])
                                    await message.reply(response.text)

                                elif attachment.filename.endswith(".txt"):
                                    sample_txt = genai.upload_file(filename, mime_type="text/plain")
                                    if message.author.id not in self.chats:
                                        self.chats[message.author.id] = self.model.start_chat()
                                    chat = self.chats[message.author.id]
                                    response = chat.send_message([question, sample_txt])
                                    await message.reply(response.text)

                                # Удаляем файл через 5 минут
                                await asyncio.sleep(300)
                                os.remove(filename)
                                return  

                        if message.author.id not in self.chats:
                            self.chats[message.author.id] = self.model.start_chat()
                        chat = self.chats[message.author.id]
                        response = chat.send_message(question)
                        await message.reply(response.text)

                    except Exception as e:
                        await message.reply(f"Ошибка: {e}")
    
    @commands.slash_command()
    async def reset_chat(self, inter: disnake.ApplicationCommandInteraction):
        """Сбрасывает текущий чат."""
        try:
            if inter.author.id in self.chats:
                del self.chats[inter.author.id]
                await inter.response.send_message("Чат сброшен.", ephemeral=True)
            else:
                await inter.response.send_message("У вас нет активного чата.", ephemeral=True)
        except Exception as e:
            await inter.response.send_message(f"Ошибка: {e}", ephemeral=True)

def setup(bot):
    bot.add_cog(App(bot))
