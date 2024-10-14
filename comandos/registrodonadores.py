import discord
from discord import app_commands
from discord.ext import commands
from google.cloud import firestore
import os

class RegistroDonadores(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = firestore.Client()

    @app_commands.command(name="registrodonadores", description="Registra una serie en la base de datos con los IDs de las carpetas Dragon y Fenix")
    @app_commands.checks.has_role(int(os.getenv("ROL_AUTORIZADO")))
    async def registro_donadores(self, interaction: discord.Interaction, serie: str, id_dragon: str, id_fenix: str):
        donadores_ref = self.db.collection(os.getenv("FIRESTORE_COLLECTION"))

        donadores_ref.add({
            "serie": serie,
            "id_dragon": id_dragon,
            "id_fenix": id_fenix
        })

        await interaction.response.send_message(f'Serie "{serie}" registrada con éxito en la base de datos.', ephemeral=True)

async def setup(bot):
    await bot.add_cog(RegistroDonadores(bot))
