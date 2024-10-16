import discord
from discord import app_commands
from discord.ext import commands
from google.cloud import firestore
import os

class RegistroDonadores(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = firestore.Client()

    @app_commands.command(name="registrodonadores", description="Registrar donadores en la base de datos")
    @app_commands.describe(serie="Nombre de la serie", id_dragon="ID de la carpeta Dragon", id_fenix="ID de la carpeta Fenix")
    @app_commands.checks.has_role(int(os.getenv("ROL_AUTORIZADO")))
    async def registro_donadores(self, interaction: discord.Interaction, serie: str, id_dragon: str, id_fenix: str):
        donadores_ref = self.db.collection(os.getenv("FIRESTORE_COLLECTION"))

        try:
            # Agregar la serie a la base de datos Firestore
            donadores_ref.add({
                "serie": serie,
                "id_dragon": id_dragon,
                "id_fenix": id_fenix
            })
            await interaction.response.send_message(f'Serie "{serie}" registrada con éxito en la base de datos.', ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error al registrar la serie: {str(e)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(RegistroDonadores(bot))
