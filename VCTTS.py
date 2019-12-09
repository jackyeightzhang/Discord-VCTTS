#TestToSpeech.py
''' Created by: Jacky Zhang (jackyeightzhang) '''
import os
import logging
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('discord_token')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='>')

@bot.command(name='hello')
async def greeting(ctx):
    await ctx.send('greeting::hello invoked')
    await bot.close()

@bot.command(name='connect')
async def connectToVC(ctx):
    voiceChannel = ctx.message.author.voice.channel
    await ctx.send(f'connectToVC::TestDiscodPyBot connecting to {voiceChannel.name}')
    await voiceChannel.connect()

@bot.command(name='disconnect')
async def disconnectFromVC(ctx):
    voiceClient = ctx.voice_client
    await ctx.send(f'disconnectFromVC::TestDiscodPyBot disconnecting {voiceClient}')
    await voiceClient.disconnect()
    
bot.run(TOKEN)
