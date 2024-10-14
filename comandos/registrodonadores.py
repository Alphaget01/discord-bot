import discord
from discord.ext import commands
from google.cloud import firestore
import os

class RegistroDonadores(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = firestore.Client()

    @commands.command()
    @commands.has_role(int(os.getenv("ROL_AUTORIZADO")))
    async def registrodonadores(self, ctx, serie: str, id_dragon: str, id_fenix: str):
        donadores_ref = self.db.collection(os.getenv("FIRESTORE_COLLECTION"))
        
        donadores_ref.add({
            "serie": serie,
            "id_dragon": id_dragon,
            "id_fenix": id_fenix
        })
        
        await ctx.send(f'Serie "{serie}" registrada con éxito en la base de datos.')

def setup(bot):
    bot.add_cog(RegistroDonadores(bot))
