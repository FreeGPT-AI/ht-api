import nextcord
from nextcord.ext import commands
from ..utils import switcher

class SwitcherCog(commands.Cog):
    """
    Cog for property switching
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @nextcord.slash_command(name="switch", description="Switches a property's status of an user.")
    async def switch(
        self,
        interaction: nextcord.Interaction,
        user: nextcord.Member = nextcord.SlashOption(description="The user to switch the property of."),
        property: str = nextcord.SlashOption(
            description="The property to switch.",
            choices={"Banned": "banned", "Premium": "premium"}
        ),
        status: bool = nextcord.SlashOption(description="The new status of the property.")
    ) -> None:
        """Switches the property's status of an user"""
        await switcher(interaction, user=user, property=property, status=status)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(SwitcherCog(bot))