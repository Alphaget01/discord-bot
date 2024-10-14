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
        await bot.tree.sync()  # Sincroniza los slash commands
        print("Comandos slash sincronizados correctamente.")
    except Exception as e:
        print(f"Error al sincronizar los comandos: {e}")

    await bot.load_extension("comandos.registrodonadores")
    await bot.load_extension("comandos.subirpdf")

bot.run(os.getenv("DISCORD_TOKEN"))
