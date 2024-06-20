import nextcord
from nextcord.ext import commands
from ..utils import generate_key, lookup

class KeyCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @nextcord.slash_command(name="key", description="...")
    async def group(self, _: nextcord.Interaction) -> None:
        """Generates an API key"""

    @group.subcommand(name="get", description="Returns your API key.")
    async def get(self, interaction: nextcord.Interaction) -> None:
        """Generates an API key"""
        await generate_key(interaction)

    @group.command(name="reset", description="Resets your API key.")
    async def reset(self, interaction: nextcord.Interaction) -> None:
        """Resets an API key"""
        await generate_key(interaction, reset=True)

    @group.command(name="lookup", description="Returns the API info about a user.")
    async def lookup(
        self,
        interaction: nextcord.Interaction,
        user: nextcord.Member = nextcord.SlashOption(description="The user to look up.")
    ) -> None:
        """Looks up the API info about a user"""
        await lookup(interaction, user=user)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(KeyCog(bot))