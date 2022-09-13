import asyncio
import os

import discord
from discord import utils
from discord.ext import commands

from commands.assign import assign
from commands.ping import ping
from commands.sign_up import sign_up
from commands.open import open
from commands.view import view
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
    bot.tree.add_command(open)
    bot.tree.add_command(view)
    bot.tree.add_command(assign)
    
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
