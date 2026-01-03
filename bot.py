import discord
from discord.ext import commands
from discord import app_commands
import json, random, os
from dotenv import load_dotenv

from game.logic import evaluate_guess
from ui.embeds import build_wordle_embed
from utils.helpers import convert_to_year
from utils.daily import  get_daily_champion, get_today_str
from ui.game_buttons import GameActionView, GameEndView
from db.rank_db import save_rank, init_db, has_played_today
from ui.rank_view import RankView
from ui.rank_embed import build_rank_embed

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

with open("Loldle/champions_data.json", encoding="utf-8") as f:
    CHAMPS = json.load(f)

CHAMP_BY_NAME = {
    c["championName"].lower(): c
    for c in CHAMPS
}

CHAMPION_NAMES = sorted(c["championName"] for c in CHAMPS)

sessions = {}

async def champion_autocomplete(
    interaction: discord.Interaction,
    current: str,
):
    current = current.lower()
    matches = [
        name for name in CHAMPION_NAMES
        if name.lower().startswith(current)
    ][:10]

    return [
        app_commands.Choice(name=name, value=name)
        for name in matches
    ]

async def start_new_game(interaction: discord.Interaction):
    user_id = interaction.user.id
    today = get_today_str()

    session = sessions.get(user_id)

    if has_played_today(user_id, today):
        await interaction.response.send_message(
            "❌ Chơi ít thôi, mai chơi tiếp",
            ephemeral=True
        )
        return

    if session and session["date"] == today:
        await interaction.response.send_message(
            "❌ Chơi ít thôi, mai chơi tiếp",
            ephemeral=True
        )
        return

    daily_champ = get_daily_champion(CHAMPS)

    sessions[user_id] = {
        "date": today,
        "answer": daily_champ,
        "tries": 0,
        "history": [],
        "finished": False
    }

    await interaction.response.send_message(
        f"🎮 Dùng `/guess <tên tướng>` để đoán.",
        ephemeral=True
    )


@bot.event
async def on_ready():
    init_db()
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()

@bot.tree.command(name="loldle_start", description="Bắt đầu game LoLdle")
async def start(interaction: discord.Interaction):
    await start_new_game(interaction)

@bot.tree.command(name="rank", description="Xem LoLdle rank theo ngày")
async def rank(interaction: discord.Interaction):
    today = get_today_str()
    embed = build_rank_embed(today)

    await interaction.response.send_message(
        embed=embed,
        view=RankView(today)
    )

@bot.tree.command(name="guess", description="Đoán tướng")
@app_commands.autocomplete(name=champion_autocomplete)
async def guess(interaction: discord.Interaction, name: str):
    await interaction.response.defer()

    user_id = interaction.user.id
    session = sessions[user_id]
    if session["finished"]:
        await interaction.followup.send(
            "❌ Chơi ít thôi, mai chơi tiếp",
            ephemeral=True
        )
        return

    if user_id not in sessions:
        await interaction.followup.send(
            "Chưa bắt đầu game. Dùng `/loldle_start`",
            ephemeral=True
        )
        return

    guess = CHAMP_BY_NAME.get(name.lower())
    if not guess:
        await interaction.followup.send(
            "Không tìm thấy tướng",
            ephemeral=True
        )
        return

    session["tries"] += 1
    answer = session["answer"]

    year_guess = convert_to_year(guess["release_date"])
    year_answer = convert_to_year(answer["release_date"])

    evaluation = evaluate_guess(guess, answer, year_guess, year_answer)
    embed = build_wordle_embed(guess, answer, session["tries"], evaluation)

    # WIN
    if guess["championName"] == answer["championName"]:
        session["finished"] = True
        embed.title = f"🎉 Chính xác! Đáp án là **{answer['championName']}**"
        embed.color = discord.Color.green()

        await interaction.followup.send(
            embed=embed,
            view=GameEndView(interaction.user.id, start_new_game)
        )
        return

    # LOSE
    if session["tries"] >= 10:
        session["finished"] = True
        await interaction.followup.send(
            f"🐔 Gà điên, đáp án là **{answer['championName']}**",
            view=GameEndView(interaction.user.id, start_new_game)
        )
        return

    save_rank(
        user_id=interaction.user.id,
        username=interaction.user.display_name,
        date=session["date"],
        tries=session["tries"],
        finished=1
    )

    await interaction.followup.send(
        embed=embed,
        view=GameActionView(
            interaction.user.id,
            sessions,
            start_new_game
        )
    )



bot.run(TOKEN)
