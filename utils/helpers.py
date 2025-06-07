import aiohttp
import discord
from dotenv import load_dotenv
import os
import io

load_dotenv(r"C:\Users\angie\The Creators Public\creatorcore-bot\data\.env")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

# Helper: call ElevenLabs TTS API to get audio bytes
async def text_to_speech(text: str) -> bytes:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    json_data = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=json_data) as resp:
            if resp.status != 200:
                return None # type: ignore
            return await resp.read()

# Helper: play audio in voice channel
async def play_audio_in_voice(ctx, audio_bytes: bytes, bot):
    if not ctx.author.voice or not ctx.author.voice.channel:
        await ctx.respond("You need to be in a voice channel to play audio.", ephemeral=True)
        return
    voice_channel = ctx.author.voice.channel
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_connected(): # type: ignore
        if voice_client.channel != voice_channel:
            await voice_client.move_to(voice_channel) # type: ignore
    else:
        voice_client = await voice_channel.connect()
    audio_source = discord.FFmpegPCMAudio(io.BytesIO(audio_bytes), pipe=True)
    if voice_client.is_playing(): # type: ignore
        voice_client.stop() # type: ignore
    voice_client.play(audio_source) # type: ignore
    await ctx.respond("Playing the response in voice channel.")
