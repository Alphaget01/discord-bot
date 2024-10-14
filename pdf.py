import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
from pathlib import Path

# Cargar el archivo .env desde la ruta específica
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Intents necesarios para el bot
intents = discord.Intents.default()
intents.message_content = True  # Permitir leer contenido de los mensajes
intents.guilds = True  # Habilitar eventos relacionados con servidores

# Configuración del bot
bot = commands.Bot(command_prefix="/", intents=intents)

# Verificar que DISCORD_GUILD_ID esté cargado
GUILD_ID = os.getenv("DISCORD_GUILD_ID")
print(f"DISCORD_GUILD_ID: {GUILD_ID}")  # Depuración
print(f"DISCORD_TOKEN: {os.getenv('DISCORD_TOKEN')}")  # Depuración

@bot.event
async def on_ready():
    print(f'{bot.user.name} ha iniciado sesión en Discord')

    # Sincronización de comandos slash en un servidor específico
    try:
        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))  # Asegurarse de que el ID esté definido
            synced = await bot.tree.sync(guild=guild)  # Sincronizar solo para este servidor
            print(f"Comandos slash sincronizados correctamente para la guild {GUILD_ID}: {len(synced)} comandos.")
            for command in synced:
                print(f"Comando sincronizado: {command.name}")
        else:
            print("Error: DISCORD_GUILD_ID no está definido correctamente.")
    except discord.errors.HTTPException as e:
        print(f"Error HTTP al sincronizar comandos slash: {e.status} - {e.text}")
    except Exception as e:
        print(f"Error al sincronizar comandos slash: {e}")

    # Cargar extensiones (comandos)
    try:
        await bot.load_extension("comandos.registrodonadores")
        await bot.load_extension("comandos.subirpdf")
        print("Comandos cargados correctamente.")
    except commands.ExtensionError as e:
        print(f"Error al cargar las extensiones: {e.name} - {e.original}")
    except Exception as e:
        print(f"Error al cargar los comandos: {e}")

# Ejecutar el bot con el token de Discord desde el archivo .env
bot.run(os.getenv("DISCORD_TOKEN"))
