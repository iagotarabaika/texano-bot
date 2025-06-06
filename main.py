import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("✅ Joined the voice channel.")
    else:
        await ctx.send("❌ You're not in a voice channel.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Left the voice channel.")
    else:
        await ctx.send("❌ I'm not in a voice channel.")

@bot.command()
async def play(ctx, url):
    if not ctx.voice_client:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("❌ You're not in a voice channel.")
            return

    vc = ctx.voice_client

    if vc.is_playing():
        vc.stop()

    ffmpeg_options = {
        'options': '-vn -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
    }

    source = discord.FFmpegPCMAudio(url, **ffmpeg_options)
    vc.play(source, after=lambda e: print(f"✅ Stream ended: {e}"))
    await ctx.send(f"🎵 Now playing: {url}")

# Read the token from Railway environment variable
TOKEN = os.environ["DISCORD_TOKEN"]
bot.run(TOKEN)
