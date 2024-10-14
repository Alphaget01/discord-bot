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
    async def subir_pdf(self, interaction: discord.Interaction, images: discord.Attachment, serie: str, chapter: int):
        # Validar que el archivo sea una imagen
        if not images.content_type.startswith("image/"):
            await interaction.response.send_message("Por favor adjunta un archivo de imagen válido (JPEG, PNG, etc).", ephemeral=True)
            return

        # Descargar la imagen adjunta
        await interaction.response.send_message("Descargando imagen JPG...", ephemeral=True)
        image_path = f"./temp/{images.filename}"  # Ruta temporal para guardar la imagen

        try:
            await images.save(image_path)
            await interaction.followup.send(f"Imagen {images.filename} guardada.")
        except Exception as e:
            await interaction.followup.send(f"Error al guardar la imagen: {str(e)}")
            return

        # Paso 1: Convertir imágenes a PDF usando el script en JavaScript
        await interaction.followup.send("Convirtiendo imágenes a PDF...")

        try:
            subprocess.run(['node', './utils_js/convertir_las_imágenes_a_pdf.js'], check=True)
            await interaction.followup.send(f"Imágenes convertidas a PDF para la serie {serie}, capítulo {chapter}.")
        except subprocess.CalledProcessError as e:
            await interaction.followup.send(f"Error al convertir imágenes a PDF: {str(e)}")
            return  # Detenemos la ejecución si ocurre un error

        # Paso 2: Subir el PDF a Google Drive (esto es un ejemplo, asegúrate de tener la función correcta implementada)
        pdf_path = f"{serie}_{chapter}.pdf"
        await interaction.followup.send("Subiendo PDF a Google Drive...")
        # Implementar la función de subida a Google Drive, si aún no está
        # subir_a_drive(pdf_path, serie)

        # Paso 3: Hacer el anuncio en Discord
        embed = discord.Embed(
            title="¡PDF Subido!",
            description=f'El PDF de la serie **{serie}**, capítulo {chapter} ha sido subido a las carpetas Dragon y Fenix. Anuncios hechos.',
            color=discord.Color.green()
        )
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(SubirPDF(bot))
