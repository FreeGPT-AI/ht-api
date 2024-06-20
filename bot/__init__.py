import os
import asyncio
import nextcord
from nextcord.ext import commands

bot = commands.Bot(intents=nextcord.Intents.default(), command_prefix="penis")

async def setup(bot: commands.Bot) -> None:
    for file in os.listdir("src/bot/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            await bot.load_extension(f"src.bot.cogs.{file[:-3]}")
            
async def start() -> None:
    await setup(bot)
    await bot.start(os.environ["BOT_TOKEN"])
    
asyncio.run(start())