import sqlite3
from discord import app_commands
import discord

@app_commands.command()
@app_commands.default_permissions()
@app_commands.describe(
    open='Whether to open requests on this cycle. Defaults to true.'
)
async def open(interaction: discord.Interaction, open: bool=True):
    open = 1 if open else 0

    with sqlite3.connect('database.sqlite3') as db:
        phase, currently_open = db.execute("SELECT MAX(phase), active FROM current_phase;").fetchone()

        if currently_open == open:
            return await interaction.response.send_message(embed=discord.Embed(
                title=f'Phase is already {"open" if open else "closed"}',
                description='No change has been made to the phase\'s state',
                color=discord.Color.red(),
            ))

        db.execute("""
            UPDATE current_phase
                SET active = :active
                WHERE phase = :phase;
        """, {
            'active': open,
            'phase': phase,
        })

        return await interaction.response.send_message(embed=discord.Embed(
            title=f"Phase {'opened' if open else 'closed'}",
            description='Phase updated.',
            color=discord.Color.green(),
        ))