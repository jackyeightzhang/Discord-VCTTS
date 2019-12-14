#TestToSpeech.py
''' Created by: Jacky Zhang (jackyeightzhang) '''
import os
import logging
from dotenv import load_dotenv
from discord.ext import commands
from discord import FFmpegPCMAudio
from google.cloud import texttospeech

load_dotenv()
TOKEN = os.getenv('discord_token')

GOOGLE_APPLICATION_CREDENTIALS = os.getenv('google_application_credentials')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = commands.Bot(command_prefix='>')

#check to see if the bot is functional
@bot.command(name='hello')
async def greeting(ctx):
    await ctx.send('greeting::hello invoked')
    await bot.close()

#connect bot to the voice chat that the user is in
@bot.command(name='connect')
async def connectToVC(ctx):
    voiceChannel = ctx.message.author.voice.channel
    await ctx.send(f'connectToVC::TestDiscodPyBot connecting to {voiceChannel.name}')
    await voiceChannel.connect()

#disconnect bot from voice chat
@bot.command(name='disconnect')
async def disconnectFromVC(ctx):
    voiceClient = ctx.voice_client
    await ctx.send(f'disconnectFromVC::TestDiscodPyBot disconnecting {voiceClient.user}')
    await voiceClient.disconnect()

#bot says hello world in chat
@bot.command(name='sayhello')
async def sayHello(ctx):
    googleClient = texttospeech.TextToSpeechClient.from_service_account_json(GOOGLE_APPLICATION_CREDENTIALS)
    synthesis_input = texttospeech.types.SynthesisInput(text="Hello!")
    voice = texttospeech.types.VoiceSelectionParams(
    language_code='en-US',
    ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.types.AudioConfig(
    audio_encoding=texttospeech.enums.AudioEncoding.OGG_OPUS)
    response = googleClient.synthesize_speech(synthesis_input, voice, audio_config)

    voiceClient = ctx.voice_client
    with open('output.mp3', 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')
    audioSource = FFmpegPCMAudio('output.mp3')
    voiceClient.play(audioSource)
    print('done')
bot.run(TOKEN)
