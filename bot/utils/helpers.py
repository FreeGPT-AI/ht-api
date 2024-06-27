import nextcord
from .users import UserManager

async def generate_key(interaction: nextcord.Interaction, reset: bool = False):
    """Generates an API key for an user"""
    
    await interaction.response.defer(ephemeral=True)

    check_key = await UserManager.check_key(interaction.user.id)

    if reset:
        if check_key is None:
            return await interaction.followup.send("You don't have an API key.", ephemeral=True)
        await UserManager.delete_key(interaction.user.id)
        premium = check_key.premium
    elif check_key is not None:
        return await interaction.followup.send(f"Your API key is: {check_key.key}", ephemeral=True)
    else:
        premium = False
    
    generated_key = await UserManager.create_key(interaction.user.id, premium)
    await interaction.followup.send(f"Your new API key is: {generated_key}", ephemeral=True)

async def switcher(interaction: nextcord.Interaction, user: nextcord.Member, property: str, status: bool):
    """Switches the property's status of an user"""

    await interaction.response.defer(ephemeral=True)

    if not interaction.user.guild_permissions.manage_guild:
        return await interaction.followup.send("You do not have permission to use this command.", ephemeral=True)

    check_key = await UserManager.check_key(interaction.user.id)

    if check_key is None:
        return await interaction.followup.send("This user does not have an API key.", ephemeral=True)
        
    await UserManager.set_property(interaction.user.id, property, status)
    action = "banned" if property == "banned" and status else "unbanned" if property == "banned" else "gave" if property == "premium" and status else "removed"
    await interaction.followup.send(f"Successfully {action} {user.mention}.", ephemeral=True)