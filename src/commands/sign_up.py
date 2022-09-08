import sqlite3
import discord
from discord import app_commands

from country import Country

@app_commands.command(name='sign-up')
async def sign_up(
    interaction: discord.Interaction,
    first_country: Country,
    second_country: Country=None,
    third_country: Country=None,
    fourth_country: Country=None,
    fifth_country: Country=None,
):
    requested_countries = [first_country, second_country, third_country, fourth_country, fifth_country]
    requested_countries = [country for country in requested_countries if country is not None]

    unique_countries = set(requested_countries)

    if len(unique_countries) != len(requested_countries):
        return await interaction.response.send_message(embed=discord.Embed(
            title='Cannot request the same country twice',
            description='You cannot request the same country more than once.',
            color=discord.Color.red(),
        ))

    with sqlite3.connect("database.sqlite3") as db:
        phase, active = db.execute("SELECT MAX(phase), active FROM current_phase;").fetchone()

        if active == 0:
            return await interaction.response.send_message(embed=discord.Embed(
                title='Phase not open',
                description='You cannot currently request countries. Try again later.',
                color=discord.Color.red(),
            ))

        existing = db.execute("""
            SELECT COUNT(*)
                FROM requests
                WHERE
                    user_id = :user_id AND
                    phase = :phase;
        """, {
            'user_id': interaction.user.id,
            'phase': phase,
        }).fetchone()[0]

        if existing > 0:
            return await interaction.response.send_message(embed=discord.Embed(
                title='Already requested countries',
                description="You've already requested your countries.",
                color=discord.Color.red(),
            ))

        other_requests = db.execute("""
            SELECT COUNT(*)
                FROM requests
                WHERE
                    phase = :phase;
        """, {
            'phase': phase,
        }).fetchone()[0]

        if other_requests >= len(Country):
            return await interaction.response.send_message(embed=discord.Embed(
                title='Maximum number of countries reached',
                description='There are no longer any countries left to assign.',
                color=discord.Color.red(),
            ))

        id = db.execute("""
            INSERT INTO requests (
                user_id, phase
            ) VALUES (
                :user_id,
                :phase
            ) RETURNING id;
        """, {
            'user_id': interaction.user.id,
            'phase': phase,
        }).fetchone()[0]

        for score, country in enumerate(requested_countries):
            db.execute("""
                INSERT INTO request_content (
                    request_id, content, score
                ) VALUES (
                    :id,
                    :content,
                    :score
                )
            """, {
                'id': id,
                'content': country.value,
                'score': score,
            })

    await interaction.response.send_message(embed=discord.Embed(
        title='Registered request',
        description='Your request has been registered.',
        color=discord.Color.green(),
    ))
