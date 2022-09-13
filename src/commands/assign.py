import random
import sqlite3
import discord
from discord import app_commands

from country import Country


@app_commands.command()
async def assign(interaction: discord.Interaction):
    with sqlite3.connect("database.sqlite3") as db:
        phase = db.execute("SELECT MAX(phase) FROM current_phase;").fetchone()[0]

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


        if not requests:
            return await interaction.response.send_message(embed=discord.Embed(
                title='No requests yet',
                description='There have not been any requests submitted since the last assignment.',
                color=discord.Color.red(),
            ))

        assignments = solve(requests)

        newline = '\n'

        await interaction.response.send_message(f"""
{newline.join(f'<@!{id}>: {country.value}' for id, country in assignments.items())}
""")

        db.execute("""
            INSERT INTO current_phase (phase, active)
            VALUES (:phase, 0)
        """, {
            'phase': phase + 1,
        })


def solve(requests: list[tuple[int, str, int]]) -> dict[int, Country]:
    ids = set(id for id, _, __ in requests)
    requests = [
        (id, Country(raw_country), score) for id, raw_country, score in requests
    ]
    available_countries = list(Country)

    assignments: dict[int, Country] = {}

    max_score = 0

    while len(requests) > 0:
        # Score is 3rd element in request
        top_requests = [request for request in requests if request[2] <= max_score]

        # If there are no requests left with the current score, increment the minimum score and move
        # to the next iteration.
        if len(top_requests) == 0:
            max_score += 1
            continue

        # Get a country from the list of available countries and requests that match it.
        current_country = available_countries.pop(0)
        matching_requests = [request for request in top_requests if request[1] == current_country]

        # If there are no requests matching this country, nobody wants it (within the current max
        # score), add it back to the list of available countries and move on.
        if len(matching_requests) == 0:
            available_countries.append(current_country)
            continue

        # If there are people that want the country, assign it to a random one.
        assignment = random.choice(matching_requests)
        assignments[assignment[0]] = current_country

        # Remove all requests for this country and user.
        for request in list(requests):
            if request[1] == current_country or request[0] == assignment[0]:
                requests.remove(request)

    if len(assignments) < len(ids):
        for id in random.shuffle(list(ids)):
            if id not in assignments:
                assignments[id] = available_countries.pop()

    return assignments
