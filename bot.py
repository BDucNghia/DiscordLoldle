import discord
from discord.ext import commands
from discord import app_commands
import json, random, os
from dotenv import load_dotenv

from game.logic import evaluate_guess
from ui.embeds import build_wordle_embed
from utils.helpers import convert_to_year

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

# ======================
# AUTOCOMPLETE
# ======================
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

# ======================
# EVENTS
# ======================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()

# ======================
# COMMANDS
# ======================
@bot.tree.command(name="loldle_start", description="Bắt đầu game LoLdle")
async def start(interaction: discord.Interaction):
    sessions[interaction.user.id] = {
        "answer": random.choice(CHAMPS),
        "tries": 0
    }

    await interaction.response.send_message(
        "**LoLdle bắt đầu!**\nDùng `/guess <tên tướng>`",
        ephemeral=True
    )

@bot.tree.command(name="guess", description="Đoán tướng")
@app_commands.autocomplete(name=champion_autocomplete)
async def guess(interaction: discord.Interaction, name: str):
    user_id = interaction.user.id

    if user_id not in sessions:
        await interaction.response.send_message(
            "Chưa bắt đầu game. Dùng `/loldle_start`",
            ephemeral=True
        )
        return

    session = sessions[user_id]
    session["tries"] += 1

    answer = session["answer"]
    guess = CHAMP_BY_NAME.get(name.lower())

    if not guess:
        await interaction.response.send_message("Không tìm thấy tướng")
        return

    year_guess = convert_to_year(guess["release_date"])
    year_answer = convert_to_year(answer["release_date"])

    evaluation = evaluate_guess(guess, answer, year_guess, year_answer)
    embed = build_wordle_embed(guess, answer, session["tries"], evaluation)

    # WIN
    if guess["championName"] == answer["championName"]:
        del sessions[user_id]
        embed.title = "Onii-chan giỏi quá!!!"
        embed.title = f"🎉 {answer['championName']} 🎉"
        embed.color = discord.Color.green()
        await interaction.response.send_message(embed=embed)
        return

    # LOSE
    if session["tries"] >= 10:
        del sessions[user_id]
        await interaction.response.send_message(
            f"Gà điên, đáp án là **{answer['championName']}**"
        )
        return

    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)
