import discord
import os

async def hacer_anuncio(ctx, serie, chapter):
    guild = ctx.guild

    # Obtener los canales y roles
    canal_anuncios_1 = guild.get_channel(int(os.getenv("CANAL_ANUNCIOS_1")))
    rol_anuncios_1 = guild.get_role(int(os.getenv("ROL_ANUNCIOS_1")))

    embed = discord.Embed(
        title=f"Nuevo capítulo de {serie}",
        description=f"Capítulo {chapter} disponible en Google Drive.",
        color=discord.Color.blue()
    )
    embed.add_field(name="Link", value=f"https://drive.google.com/drive/folders/...", inline=False)

    # Enviar el anuncio en el primer canal
    await canal_anuncios_1.send(f"{rol_anuncios_1.mention}", embed=embed)
