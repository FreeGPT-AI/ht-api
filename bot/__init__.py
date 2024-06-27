import os
import nextcord
from nextcord.ext import commands

bot = commands.Bot(intents=nextcord.Intents.default())

@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

def setup(bot: commands.Bot) -> None:
    for file in os.listdir("bot/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"bot.cogs.{file[:-3]}")
            
def start() -> None:
    setup(bot)
    bot.run(os.environ["BOT_TOKEN"])
    
start()