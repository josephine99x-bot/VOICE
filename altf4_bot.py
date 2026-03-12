import os
import discord
import random
import asyncio
from discord.ext import tasks, commands
from datetime import datetime, timedelta
from gtts import gTTS

TOKEN = os.environ["TOKEN"]
CHANNEL_ID = 1479700883444076596

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

blood_start = (4, 0)
devil_start = (4, 30)
interval = 120
king_hour = 20


def now_local():
    return datetime.utcnow() - timedelta(hours=3)


def next_event(start_hour, start_minute):
    now = now_local()
    start_today = now.replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)

    while start_today < now:
        start_today += timedelta(minutes=interval)

    return start_today


@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    check_events.start()


async def anunciar_en_voz(mensaje):

    for canal in bot.guilds[0].voice_channels:

        if len(canal.members) > 0:

            if bot.voice_clients:
                vc = bot.voice_clients[0]
                await vc.move_to(canal)
            else:
                vc = await canal.connect()

            tts = gTTS(mensaje, lang="es")
            tts.save("evento.mp3")

            vc.play(discord.FFmpegPCMAudio(source="test.mp3"))

            while vc.is_playing():
                await asyncio.sleep(1)

            await vc.disconnect()
            await asyncio.sleep(2)


@tasks.loop(minutes=1)
async def check_events():

    channel = bot.get_channel(CHANNEL_ID)
    now = now_local()

    blood_next = next_event(*blood_start)
    devil_next = next_event(*devil_start)

    if 540 < (blood_next - now).total_seconds() <= 600:
        await channel.send("@everyone ⚔️ Blood Castle en 10 minutos!")
        await anunciar_en_voz("Blood Castle comienza en diez minutos")

    if 540 < (devil_next - now).total_seconds() <= 600:
        await channel.send("@everyone 👿 Devil Square en 10 minutos!")
        await anunciar_en_voz("Devil Square comienza en diez minutos")

    if now.hour == 19 and now.minute == 50:
        await channel.send("@everyone 👑 King of MU comienza en 10 minutos!")
        await anunciar_en_voz("King of Mu comienza en diez minutos")


@bot.command()
async def anunciar_en_voz(mensaje):

    guild = bot.guilds[0]

    for canal in guild.voice_channels:

        if len(canal.members) > 0:

            if bot.voice_clients:
                vc = bot.voice_clients[0]
                await vc.move_to(canal)
            else:
                vc = await canal.connect()

            tts = gTTS(mensaje, lang="es")
            tts.save("evento.mp3")

            vc.play(discord.FFmpegPCMAudio(source="evento.mp3"))

            while vc.is_playing():
                await asyncio.sleep(1)

            await vc.disconnect()
            await asyncio.sleep(2)

@bot.command()
async def ruleta(ctx, *jugadores):

    if len(jugadores) < 2:
        await ctx.send("⚠️ Tenés que mencionar al menos 2 jugadores.")
        return

    participantes = list(jugadores)

    mensaje = await ctx.send("🎰 **Girando la ruleta ALT F4...**")

    for i in range(5):
        elegido = random.choice(participantes)
        await mensaje.edit(content=f"🎰 Girando... {elegido}")
        await asyncio.sleep(1)

    ganador = random.choice(participantes)

    await mensaje.edit(content=f"""
🎰 **RULETA ALT F4**

Participantes:
{' '.join(participantes)}

🏆 **GANADOR:** {ganador}
""")


bot.run(TOKEN)




