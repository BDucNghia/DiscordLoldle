# ui/rank_view.py
import discord
from discord.ui import View, Button
from datetime import datetime, timedelta
from ui.rank_embed import build_rank_embed


class RankView(View):
    def __init__(self, date_str: str):
        super().__init__(timeout=180)
        self.date = datetime.fromisoformat(date_str).date()

    @discord.ui.button(label="⬅", style=discord.ButtonStyle.secondary)
    async def prev_day(self, interaction: discord.Interaction, button: Button):
        self.date -= timedelta(days=1)
        await self.update(interaction)

    @discord.ui.button(label="➡", style=discord.ButtonStyle.secondary)
    async def next_day(self, interaction: discord.Interaction, button: Button):
        self.date += timedelta(days=1)
        await self.update(interaction)

    async def update(self, interaction: discord.Interaction):
        embed = build_rank_embed(self.date.isoformat())
        await interaction.response.edit_message(
            embed=embed,
            view=self
        )
