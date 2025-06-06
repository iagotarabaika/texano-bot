import os
import json
import discord
from discord.ext import commands

# Caminho para o arquivo JSON com as estações
STATIONS_FILE = "stations.json"

# Carrega as estações do arquivo JSON ou cria um padrão se não existir
if os.path.exists(STATIONS_FILE):
    with open(STATIONS_FILE, "r", encoding="utf-8") as f:
        ESTACOES = json.load(f)
else:
    ESTACOES = {
        "forro": "http://stm16.xcast.com.br:10582/stream",
        "105.1": "https://www.appradio.app:8010/live",
        "club": "https://8157.brasilstream.com.br/stream",
        "pagode": "https://stm15.xcast.com.br:12534/stream"
    }
    with open(STATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(ESTACOES, f, indent=2, ensure_ascii=False)

# Discord setup
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logado como {bot.user}")

@bot.command()
async def tocar(ctx, nome: str):
    if ctx.author.voice:
        url = ESTACOES.get(nome.lower())
        if not url:
            await ctx.send("❌ Estação não encontrada.")
            return

        canal = ctx.author.voice.channel
        if ctx.voice_client is None:
            vc = await canal.connect()
        else:
            vc = ctx.voice_client
            if vc.channel != canal:
                await vc.move_to(canal)

        if vc.is_playing():
            vc.stop()

        ffmpeg_options = {
            'options': '-vn -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
        }

        source = discord.FFmpegPCMAudio(url, **ffmpeg_options)
        vc.play(source)
        await ctx.send(f"📻 Tocando agora: **{nome.title()}**")
    else:
        await ctx.send("❌ Você precisa estar em um canal de voz para tocar rádio.")

@bot.command()
async def parar(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("⛔ Rádio parada.")
    else:
        await ctx.send("❌ Não estou em um canal de voz.")

@bot.command()
async def menu(ctx):
    lista = '\n'.join([f"- `{nome}`" for nome in ESTACOES.keys()])
    texto = (
        "**🎶 Comandos disponíveis:**\n"
        "`!tocar [nome]` - Toca uma estação\n"
        "`!parar` - Para de tocar e sai\n"
        "`!menu` - Mostra este menu\n"
        "`!adicionar [nome] [url]` - Adiciona nova estação\n\n"
        "**📡 Estações disponíveis:**\n"
        f"{lista}"
    )
    await ctx.send(texto)

@bot.command()
async def adicionar(ctx, nome: str, url: str):
    nome = nome.lower()
    if nome in ESTACOES:
        await ctx.send("⚠️ Esta estação já existe.")
        return

    ESTACOES[nome] = url
    with open(STATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(ESTACOES, f, indent=2, ensure_ascii=False)

    await ctx.send(f"✅ Estação `{nome}` adicionada com sucesso!")

# Use Railway ENV variable
TOKEN = os.environ["DISCORD_TOKEN"]
bot.run(TOKEN)
