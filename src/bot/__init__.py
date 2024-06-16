import nextcord
import yaml
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from .utils import generate_key, lookup, switcher

bot = commands.Bot(intents=nextcord.Intents.default())

with open("values/secrets.yml", "r") as f:
    config = yaml.safe_load(f)["bot"]

@bot.event
async def on_ready():
    print("Bot is online!")

@bot.slash_command(name="key")
async def main(_: Interaction):
    pass

@main.subcommand(name="get", description="Returns your API key.")
async def get_key(interaction: Interaction):
    return await generate_key(interaction)

@main.subcommand(name="reset", description="Resets your API key.")
async def reset_key(interaction: Interaction):
    return await generate_key(interaction, reset=True)

@bot.slash_command(name="lookup", description="Returns the API info about an user.")
async def reset_key(interaction: Interaction, user: nextcord.Member = SlashOption(description="The user to lookup.", required=False)):
    return await lookup(interaction, user=user)

@bot.slash_command(name="ban", description="Switches the ban status of an user.")
async def reset_key(interaction: Interaction, user: nextcord.Member = SlashOption(description="The user to ban or unban."), status: bool = SlashOption(description="The new ban status of the user.")):
    return await switcher(interaction, user=user, banned=status)

@bot.slash_command(name="premium", description="Switches the premium status of an user.")
async def reset_key(interaction: Interaction, user: nextcord.Member = SlashOption(description="The user to give or remove premium."), status: bool = SlashOption(description="The new premium status of the user.")):
    return await switcher(interaction, user=user, premium=status)

bot.run(config["token"])