import sqlite3
from discord import app_commands
import discord

@app_commands.command()
@app_commands.default_permissions()
async def view(interaction: discord.Interaction):
    with sqlite3.connect('database.sqlite3') as db:
        phase = db.execute('SELECT MAX(phase) FROM current_phase;').fetchone()[0]

        requests = db.execute("""
            SELECT 
                requests.user_id, request_content.content, request_content.score
            FROM
                requests, request_content
            WHERE
                requests.phase == :phase
                AND requests.id == request_content.request_id;

        """, {
            'phase': phase,
        }).fetchall()

        requests_mapped = {
            id: [] for id, _, __ in requests
        }

        for request in requests:
            requests_mapped[request[0]].append((request[1], request[2]))

        requests_sorted = {
            id: [
                # Copy mapped requests, sort by score and discard score
                country
                for country, _
                in sorted(requests, key=lambda request: request[1])]
                for id, requests in requests_mapped.items()
        }

        request_strings = [
            f'- <@!{id}>: {", ".join(requests)}' for id, requests in requests_sorted.items()
        ]

        newline = '\n'

        await interaction.response.send_message(
f"""
__Requests:__
{newline.join(request_strings)}
""",
            allowed_mentions=discord.AllowedMentions.none(),
        )

