# ui/embeds.py
import discord
from utils.helpers import convert_to_year

def build_wordle_embed(guess, answer, tries, evaluation):
    year_guess = convert_to_year(guess["release_date"])

    embed = discord.Embed(
        title=f"🎯 {guess['championName']}",
        color=discord.Color.dark_grey()
    )

    embed.add_field(
        name="Kết quả",
        value="\n".join([
            f"{evaluation['gender']} **Gender**: {guess['gender']}",
            f"{evaluation['positions']} **Positions**: {' | '.join(guess['positions'])}",
            f"{evaluation['species']} **Species**: {' | '.join(guess['species'])}",
            f"{evaluation['resource']} **Resource**: {guess['resource']}",
            f"{evaluation['range_type']} **Range Type**: {' | '.join(guess['range_type'])}",
            f"{evaluation['regions']} **Region(s)**: {' | '.join(guess['regions'])}",
            f"{evaluation['year']} **Release Year**: {year_guess}",
        ]),
        inline=False
    )

    embed.set_footer(text=f"Tries: {tries}/10")
    return embed
