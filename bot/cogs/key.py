import nextcord
from nextcord.ext import commands
from ..utils import generate_key

class KeyCog(commands.Cog):
    """
    Cog for key management
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @nextcord.slash_command(name="key", description="...")
    async def group(self, _: nextcord.Interaction) -> None:
        """Manages API keys"""
        pass

    @group.subcommand(name="get", description="Returns your API key.")
    async def get(self, interaction: nextcord.Interaction) -> None:
        """Generates an API key"""
        await generate_key(interaction)

    @group.subcommand(name="reset", description="Resets your API key.")
    async def reset(self, interaction: nextcord.Interaction) -> None:
        """Resets an API key"""
        await generate_key(interaction, reset=True)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(KeyCog(bot))