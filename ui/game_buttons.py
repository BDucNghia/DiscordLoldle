import discord
from discord.ui import View, Button

class GameEndView(View):
    def __init__(self, user_id, start_new_game_callback):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.start_new_game_callback = start_new_game_callback

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "❌ Đây không phải game của bạn",
                ephemeral=True
            )
            return False
        return True

    @discord.ui.button(
        label="🔁 New game",
        style=discord.ButtonStyle.primary
    )
    async def new_game(
        self,
        interaction: discord.Interaction,
        button: Button
    ):
        await self.start_new_game_callback(interaction)


class GameActionView(View):
    def __init__(self, user_id, sessions, start_new_game_callback):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.sessions = sessions
        self.start_new_game_callback = start_new_game_callback

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "❌ Đây không phải game của bạn",
                ephemeral=True
            )
            return False
        return True

    @discord.ui.button(
        label="🏳️ Give up",
        style=discord.ButtonStyle.danger
    )
    async def give_up(
        self,
        interaction: discord.Interaction,
        button: Button
    ):
        session = self.sessions.pop(self.user_id, None)
        if not session:
            await interaction.response.send_message(
                "Game đã kết thúc",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"🏳️ Lmao. Đáp án là **{session['answer']['championName']}**",
            view=GameEndView(
                interaction.user.id,
                self.start_new_game_callback
            )
        )
