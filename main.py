import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()  # Load DISCORD_TOKEN from .env

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 🎵 Saved radio stations
STATIONS = {
    "forro": "http://stm16.xcast.com.br:10582/stream",
    "example": "https://your-stream-url.com/live"  # Add more stations here
}

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# 📻 Play a radio station
@bot.command()
async def station(ctx, name: str):
    if ctx.author.voice:
        url = STATIONS.get(name.lower())
        if not url:
            await ctx.send("❌ Station not found.")
            return

        channel = ctx.author.voice.channel
        vc = await channel.connect()

        if vc.is_playing():
            vc.stop()

        ffmpeg_options = {
            'options': '-vn -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
        }

        source = discord.FFmpegPCMAudio(url, **ffmpeg_options)
        vc.play(source)
        await ctx.send(f"📻 Now playing: **{name.title()}**")
    else:
        await ctx.send("❌ You need to be in a voice channel to use this command.")

# 🛑 Stop the radio
@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("⛔ Radio stopped.")
    else:
        await ctx.send("❌ I'm not in a voice channel.")

# 📋 Show help and station list
@bot.command()
async def menu(ctx):
    station_list = '\n'.join([f"- `{name}`" for name in STATIONS.keys()])
    help_text = (
        "**🎶 Radio Bot Commands:**\n"
        "`!station [name]` - Play a saved radio station\n"
        "`!stop` - Stop the radio and leave the channel\n"
        "`!menu` - Show this help message\n\n"
        "**📡 Available Stations:**\n"
        f"{station_list}"
    )
    await ctx.send(help_text)

# 🚀 Run the bot
TOKEN = os.environ["DISCORD_TOKEN"]
bot.run(TOKEN)
