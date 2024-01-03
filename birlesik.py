from sanic import Sanic
from sanic.response import text
import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()
client = commands.Bot(command_prefix='/', intents=intents)

app = Sanic("myapp")

async def botu_başlat():
    await client.start("MTE4NjAwNTk1NzM3ODA0ODExMQ.GtiyvT.8r2V9vHzNCOTvfT2ptGfPbOPXADh6XuWRNtK78")

async def sunucuyu_başlat():
    await app.run(host='0.0.0.0', port=8000)

async def başlat():
    asyncio.create_task(botu_başlat())
    asyncio.create_task(sunucuyu_başlat())

@app.route('/')
async def merhaba(request):
    return text('Merhaba, Sanic!')

app.add_route(send_message,"/send", methods=["POST"])


if __name__ == '__main__':
    asyncio.run(başlat())
