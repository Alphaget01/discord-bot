import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} ha iniciado sesión en Discord')
    
    # Sincronizar los comandos nuevos
    try:
        await bot.tree.sync()  # Sincroniza los comandos de barra (/)
        print("Comandos sincronizados correctamente.")
    except Exception as e:
        print(f"Error al sincronizar los comandos: {e}")

    # Cargar solo los comandos que tú especificas
    await bot.load_extension("comandos.registrodonadores")
    await bot.load_extension("comandos.subirpdf")

# Iniciar el bot con el token de Discord
bot.run(os.getenv("DISCORD_TOKEN"))
