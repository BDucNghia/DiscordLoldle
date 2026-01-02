# embeds/rank_embed.py
import discord
from db.rank_db import get_rank_by_date

def build_rank_embed(date_str: str):
    rows = get_rank_by_date(date_str)

    embed = discord.Embed(
        title=f"🏆 LoLdle Rank — {date_str}",
        color=discord.Color.gold()
    )

    if not rows:
        embed.description = "Chưa có ai hoàn thành LoLdle hôm nay."
        return embed

    lines = []
    for i, row in enumerate(rows, start=1):
        if row["finished"]:
            lines.append(f"**{i}. {row['username']}** — {row['tries']} / 10")
        else:
            lines.append(f"{i}. {row['username']} — ❌")

    embed.description = "\n".join(lines)
    return embed
