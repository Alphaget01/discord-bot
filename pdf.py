import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Inicializar el bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

# Registrar los comandos
@bot.event
async def on_ready():
    print(f'{bot.user.name} ha iniciado sesión en Discord')

# Cargar los comandos desde la carpeta "comandos"
bot.load_extension("comandos.registrodonadores")
bot.load_extension("comandos.subirpdf")

# Iniciar el bot con el token de Discord
bot.run(os.getenv("DISCORD_TOKEN"))
