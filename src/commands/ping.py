import discord
from discord import app_commands

@app_commands.command()
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'Pong! Latency: `{round(interaction.client.latency * 1000)}ms`')
