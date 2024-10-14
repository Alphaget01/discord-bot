import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Intents necesarios para el bot
intents = discord.Intents.default()
intents.message_content = True  # Permitir leer contenido de los mensajes
intents.guilds = True  # Habilitar eventos relacionados con servidores

# Configuración del bot
bot = commands.Bot(command_prefix="/", intents=intents)

# ID del servidor (guild) donde sincronizar los comandos slash
GUILD_ID = os.getenv("DISCORD_GUILD_ID")

@bot.event
async def on_ready():
    print(f'{bot.user.name} ha iniciado sesión en Discord')

    # Sincronización de comandos slash en un servidor específico
    try:
        guild = discord.Object(id=int(GUILD_ID))  # Asegúrate de que sea un entero
        synced = await bot.tree.sync(guild=guild)  # Sincroniza solo para este servidor
        print(f"Comandos slash sincronizados correctamente para la guild {GUILD_ID}: {len(synced)} comandos.")
    except Exception as e:
        print(f"Error al sincronizar comandos slash: {e}")

    # Cargar extensiones (comandos)
    try:
        await bot.load_extension("comandos.registrodonadores")
        await bot.load_extension("comandos.subirpdf")
        print("Comandos cargados correctamente.")
    except Exception as e:
        print(f"Error al cargar los comandos: {e}")

# Ejecutar el bot con el token de Discord desde el archivo .env
bot.run(os.getenv("DISCORD_TOKEN"))
