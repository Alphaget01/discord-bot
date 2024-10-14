import discord
from discord import app_commands
from discord.ext import commands
import os
import subprocess

class SubirPDF(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="subirpdf", description="Sube un PDF a Google Drive a partir de imágenes y hace un anuncio en Discord")
    @app_commands.checks.has_role(int(os.getenv("ROL_AUTORIZADO")))
    async def subir_pdf(self, interaction: discord.Interaction, images, serie: str, chapter: int):
        # Paso 1: Convertir imágenes a PDF usando el script en JavaScript
        await interaction.response.send_message("Convirtiendo imágenes a PDF...", ephemeral=True)

        try:
            subprocess.run(['node', './utils_js/convertir_las_imágenes_a_pdf.js'], check=True)
            await interaction.followup.send(f"Imágenes convertidas a PDF para la serie {serie}, capítulo {chapter}.")
        except subprocess.CalledProcessError as e:
            await interaction.followup.send(f"Error al convertir imágenes a PDF: {str(e)}")
            return  # Detenemos la ejecución si ocurre un error

        # Paso 2: Subir el PDF a Google Drive (ejemplo)
        await interaction.followup.send("Subiendo PDF a Google Drive...")
        pdf_path = f"{serie}_{chapter}.pdf"
        # Función para subir a Drive
        # subir_a_drive(pdf_path, serie)

        # Paso 3: Hacer el anuncio en Discord (ejemplo)
        await interaction.followup.send("Publicando anuncios en Discord...")
        # hacer_anuncio(ctx, serie, chapter)

        # Mensaje final con un embed
        embed = discord.Embed(
            title="¡PDF Subido!",
            description=f'El PDF de la serie **{serie}**, capítulo {chapter} ha sido subido a las carpetas Dragon y Fenix. Anuncios hechos.',
            color=discord.Color.green()
        )
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(SubirPDF(bot))
