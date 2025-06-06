import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 🔊 Forró radio stream
FORRO_RADIO_URL = "https://stm01.virtualcast.com.br/forro128"

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def radio(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        vc = await channel.connect()

        if vc.is_playing():
            vc.stop()

        ffmpeg_options = {
            'options': '-vn -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
        }

        source = discord.FFmpegPCMAudio(FORRO_RADIO_URL, **ffmpeg_options)
        vc.play(source, after=lambda e: print(f"✅ Stream ended: {e}"))
        await ctx.send("🎶 Now playing Forró radio!")
    else:
        await ctx.send("❌ You need to be in a voice channel to start the radio.")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("⛔ Radio stopped.")
    else:
        await ctx.send("❌ I'm not in a voice channel.")

# 🎯 Railway token setup
TOKEN = os.environ["DISCORD_TOKEN"]
bot.run(TOKEN)
