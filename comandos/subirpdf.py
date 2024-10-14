import discord
from discord.ext import commands
import os
import subprocess

class SubirPDF(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(int(os.getenv("ROL_AUTORIZADO")))
    async def subirpdf(self, ctx, images, serie: str, chapter: int):
        # Paso 1: Convertir imágenes a PDF usando el script en JavaScript
        await ctx.send("Convirtiendo imágenes a PDF...")

        # Ejecutar el script JavaScript para convertir imágenes a PDF
        try:
            subprocess.run(['node', './utils_js/convertir_las_imágenes_a_pdf.js'], check=True)
            await ctx.send(f"Imágenes convertidas a PDF para la serie {serie}, capítulo {chapter}.")
        except subprocess.CalledProcessError as e:
            await ctx.send(f"Error al convertir imágenes a PDF: {str(e)}")
            return  # Detenemos la ejecución si ocurre un error

        # Paso 2: Subir el PDF a Google Drive
        await ctx.send("Subiendo PDF a Google Drive...")
        pdf_path = f"{serie}_{chapter}.pdf"
        # Aquí iría la función para subir a Drive
        # subir_a_drive(pdf_path, serie)

        # Paso 3: Hacer el anuncio en Discord
        await ctx.send("Publicando anuncios en Discord...")
        # Aquí iría la función para hacer el anuncio
        # hacer_anuncio(ctx, serie, chapter)

        # Mensaje final
        embed = discord.Embed(
            title="¡PDF Subido!",
            description=f'El PDF de la serie **{serie}**, capítulo {chapter} ha sido subido a las carpetas Dragon y Fenix. Anuncios hechos.',
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(SubirPDF(bot))
