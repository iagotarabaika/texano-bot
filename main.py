import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 📻 Estações de rádio salvas
ESTACOES = {
    "forro": "http://stm16.xcast.com.br:10582/stream",
    "105.1 fm": "https://www.appradio.app:8010/live",
    "radio club": "https://8157.brasilstream.com.br/stream",
    "radio pagode": "https://stm15.xcast.com.br:12534/stream"
}

@bot.event
async def on_ready():
    print(f"✅ Logado como {bot.user}")

@bot.command(name="tocar")
async def tocar(ctx, *, nome: str):
    if ctx.author.voice:
        url = ESTACOES.get(nome.lower())
        if not url:
            await ctx.send("❌ Estação não encontrada.")
            return

        canal = ctx.author.voice.channel
        vc = ctx.voice_client

        if vc and vc.is_connected():
            if vc.is_playing():
                vc.stop()
        else:
            vc = await canal.connect()

        opcoes_ffmpeg = {
            'options': '-vn -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
        }

        source = discord.FFmpegPCMAudio(url, **opcoes_ffmpeg)
        vc.play(source)
        await ctx.send(f"📻 Tocando agora: **{nome.title()}**")
    else:
        await ctx.send("❌ Você precisa estar em um canal de voz para tocar uma estação.")

@bot.command(name="parar")
async def parar(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("⛔ Rádio parada.")
    else:
        await ctx.send("❌ Não estou em um canal de voz.")

@bot.command(name="menu")
async def menu(ctx):
    lista_estacoes = '\n'.join([f"- `{nome}`" for nome in ESTACOES.keys()])
    texto_ajuda = (
        "**🎶 Comandos do bot de rádio:**\n"
        "`!tocar [nome]` - Toca uma estação de rádio\n"
        "`!parar` - Para a rádio\n"
        "`!menu` - Mostra este menu de ajuda\n\n"
        "**📡 Estações disponíveis:**\n"
        f"{lista_estacoes}"
    )
    await ctx.send(texto_ajuda)

# 🔐 Token da variável de ambiente no Railway
TOKEN = os.environ["DISCORD_TOKEN"]
bot.run(TOKEN)
