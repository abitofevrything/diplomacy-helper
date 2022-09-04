import asyncio
import os

import discord
from discord import app_commands, utils
from discord.ext import commands

async def main():
    utils.setup_logging()

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(
        command_prefix=commands.when_mentioned,
        intents=intents,
    )

    @app_commands.command()
    @app_commands.guilds(769879283677921280)
    async def pang(interaction: discord.Interaction):
        await interaction.response.send_message('Pong!')

    bot.tree.add_command(pang)

    await bot.login(os.environ['TOKEN'])
    await bot.tree.sync(guild=discord.Object(id=769879283677921280))
    await bot.connect()

if __name__ == "__main__":
    asyncio.run(main())
