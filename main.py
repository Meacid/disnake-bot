import os
import disnake
from disnake.ext import commands
import logging.config
from config import BOT_TOKEN, LOGGING_CONFIG


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logger.info("="*40)
    logger.info(f"Bot is ready!")
    logger.info(f"Bot Name: {bot.user.name}")
    logger.info(f"Bot ID: {bot.user.id}")
    logger.info(f"Bot Ping: {round(bot.latency * 1000)}ms")
    logger.info(f"Total Servers: {len(bot.guilds)}")
    logger.info("="*40)


for file in os.listdir("./cogs"):
    if file.endswith(".py"):
        try:
            bot.load_extension(f"cogs.{file[:-3]}")
            logger.info(f"Loaded extension: {file[:-3]}")
        except Exception as e:
            logger.error(f"Failed to load extension {file[:-3]}: {e}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        return
    logger.error(f"Command error: {str(error)}")

if BOT_TOKEN is None:
    logger.error("Bot token not found in environment variables!")
    exit(1)

bot.run(BOT_TOKEN)
