import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} ha iniciado sesión en Discord')
    try:
        synced = await bot.tree.sync()  # Sincroniza los slash commands
        print(f"Comandos slash sincronizados correctamente: {synced}")
    except Exception as e:
        print(f"Error al sincronizar comandos slash: {e}")

    # Carga las extensiones (comandos)
    try:
        await bot.load_extension("comandos.registrodonadores")
        await bot.load_extension("comandos.subirpdf")
        print("Comandos cargados correctamente.")
    except Exception as e:
        print(f"Error al cargar los comandos: {e}")

# Iniciar el bot con el token del archivo .env
bot.run(os.getenv("DISCORD_TOKEN"))
