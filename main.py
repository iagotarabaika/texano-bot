import os
import discord
import subprocess
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

YOUTUBE_URL = "http://stm16.xcast.com.br:10582/stream"

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

        # Get YouTube livestream audio URL
        ytdlp_cmd = ["yt-dlp", "-g", "-f", "bestaudio", YOUTUBE_URL]
        stream_url = subprocess.check_output(ytdlp_cmd).decode().strip()

        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        source = discord.FFmpegPCMAudio(stream_url, **ffmpeg_options)
        vc.play(source, after=lambda e: print(f"🔚 Stream ended: {e}"))
        await ctx.send("🎶 Now playing Forró from YouTube!")
    else:
        await ctx.send("❌ You must be in a voice channel.")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("⛔ Radio stopped.")
    else:
        await ctx.send("❌ I'm not in a voice channel.")

bot.run(os.getenv("DISCORD_TOKEN"))
