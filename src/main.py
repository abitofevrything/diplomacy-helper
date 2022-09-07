import asyncio
import os

import discord
from discord import utils
from discord.ext import commands

from commands.ping import ping
from commands.sign_up import sign_up
from database import setup_database

async def main():
    utils.setup_logging()

    setup_database()

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(
        command_prefix=commands.when_mentioned,
        intents=intents,
    )

    bot.tree.add_command(sign_up)
    bot.tree.add_command(ping)
    
    await bot.login(os.environ['TOKEN'])

    if 'GUILD' in os.environ:
        guild = discord.Object(id=int(os.environ['GUILD']))

        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
    else:
        await bot.tree.sync()
    
    await bot.connect()

if __name__ == "__main__":
    asyncio.run(main())
