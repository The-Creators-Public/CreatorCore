import os
import discord
from discord.ext import tasks
from dotenv import load_dotenv
import asyncio
import re
from typing import Optional
import sys
from datetime import datetime
import aiohttp
import io
from query_llm_ollama import query_ollama

load_dotenv(r"C:\Users\angie\The Creators Public\creatorcore-bot\.env")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_ADMIN_IDS = os.getenv("DISCORD_ADMIN_IDS")
EMERGENCY_CODE = os.getenv("EMERGENCY_CODE")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

with open(r"C:\Users\angie\The Creators Public\creatorcore-bot\instructions.txt", "r", encoding="utf-8") as f:
    instructions = f.read()


intents = discord.Intents.default()
intents.members = True

GUILD_IDS = [1379620830077517824]

bot = discord.Bot(intents=intents, guild_ids=GUILD_IDS)

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
async def play_audio_in_voice(ctx, audio_bytes: bytes):
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

# Slash command: /askcore
@bot.slash_command(name="askcore", description="Ask a question to CreatorCore and get a spoken response.")
async def askcore(ctx, prompt: str):
    await ctx.defer()
    llm_response = await query_ollama(prompt)
    if llm_response.startswith("Error:"):
        await ctx.followup.send(llm_response)
        return
    audio_bytes = await text_to_speech(llm_response)
    if not audio_bytes:
        await ctx.followup.send("Error: Failed to generate speech audio.")
        return
    if ctx.author.voice and ctx.author.voice.channel:
        await play_audio_in_voice(ctx, audio_bytes)
    else:
        audio_file = discord.File(io.BytesIO(audio_bytes), filename="response.mp3")
        await ctx.followup.send(content=llm_response, file=audio_file)


# Helper: parse duration strings like '10m', '2h', '1d' into seconds
def parse_duration(duration_str):
    match = re.match(r"(\d+)([smhd])", duration_str.lower())
    if not match:
        return None
    amount, unit = match.groups()
    amount = int(amount)
    return {"s": 1, "m": 60, "h": 3600, "d": 86400}.get(unit, 0) * amount

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})") # type: ignore

    # Notify approved users that the bot is back online
    if DISCORD_ADMIN_IDS:
        user_ids = []
        if isinstance(DISCORD_ADMIN_IDS, str):
            # Remove brackets if present and split by comma
            cleaned = DISCORD_ADMIN_IDS.strip("[]")
            user_ids = [uid.strip() for uid in cleaned.split(",")]
        elif isinstance(DISCORD_ADMIN_IDS, list):
            user_ids = DISCORD_ADMIN_IDS
        for user_id_str in user_ids:
            try:
                user_id = int(user_id_str)
                user = await bot.fetch_user(user_id)
                if user is not None:
                    try:
                        await user.send(
                            f"🟢 Bot restarted and is now online.\n"
                            f"📶 Latency: `{round(bot.latency * 1000)}ms`\n"
                        )
                    except discord.Forbidden:
                        print(f"Could not DM user {user_id}")
            except Exception as e:
                print(f"Error fetching user {user_id_str}: {e}")

# --- Slash Commands ---

@bot.command()
async def shutdown(ctx):
    admin_ids = []
    if isinstance(DISCORD_ADMIN_IDS, str):
        admin_ids = [int(uid.strip()) for uid in DISCORD_ADMIN_IDS.strip("[]").split(",")]
    elif isinstance(DISCORD_ADMIN_IDS, list):
        admin_ids = [int(uid) for uid in DISCORD_ADMIN_IDS] # type: ignore
    if ctx.author is None or ctx.author.id not in admin_ids:
        await ctx.send("You don't have permission to shut down the bot.")
        return
    await ctx.send("Shutting down...")
    await bot.close()

@bot.slash_command(name="say", description="Make the bot say a message in chat (admin only).")
async def say(ctx, message: str):
    admin_ids = []
    if isinstance(DISCORD_ADMIN_IDS, str):
        admin_ids = [int(uid.strip()) for uid in DISCORD_ADMIN_IDS.strip("[]").split(",")]
    elif isinstance(DISCORD_ADMIN_IDS, list):
        admin_ids = [int(uid) for uid in DISCORD_ADMIN_IDS] # type: ignore
    if ctx.author is None or ctx.author.id not in admin_ids:
        await ctx.respond("You don't have permission to use this command.", ephemeral=True)
        return
    await ctx.respond(message)

@bot.command()
async def restart(ctx):
    if ctx.author.id not in str(DISCORD_ADMIN_IDS):
        await ctx.send("You don't have permission to restart the bot.")
        return
    await ctx.send("Restarting...")
    
    try:
        await ctx.author.send("🔄 The bot is restarting. You'll be notified when it's back online.")
    except discord.Forbidden:
        print(f"Could not DM user {ctx.author.id}")
    
    await bot.close()
    os.execv(sys.executable, ['python'] + sys.argv)

@bot.command(name="override_shutdown")
async def override_shutdown(ctx, code: str):
    if code == EMERGENCY_CODE:
        await ctx.send("Emergency override accepted. Shutting down immediately.")
        await bot.close()
    else:
        await ctx.send("Invalid override code.")

@bot.slash_command(name="ping", description="Check the bot's latency.")
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.respond(f"Pong! Latency: {latency}ms")

@bot.slash_command(name="userinfo", description="Get info about a user.")
async def userinfo(ctx, member: Optional[discord.Member] = None):
    member = member or ctx.author
    roles = [role.name for role in member.roles if role.name != "@everyone"]
    embed = discord.Embed(title=f"{member}", color=member.color)
    if member.avatar:
        embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="ID", value=str(member.id))
    joined = member.joined_at.strftime("%Y-%m-%d %H:%M:%S") if member.joined_at else "Unknown"
    embed.add_field(name="Joined Server", value=joined)
    embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"))
    embed.add_field(name="Roles", value=", ".join(roles) if roles else "None")
    await ctx.respond(embed=embed)

@bot.slash_command(name="serverinfo", description="Display server information.")
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"{guild.name}", description=guild.description or "No description", color=discord.Color.blue())
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="Owner", value=str(guild.owner))
    embed.add_field(name="Members", value=guild.member_count)
    embed.add_field(name="Roles", value=str(len(guild.roles)))
    embed.add_field(name="Channels", value=str(len(guild.channels)))
    await ctx.respond(embed=embed)

@bot.slash_command(name="clear", description="Clear a number of messages.")
@discord.default_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    if amount < 1 or amount > 100:
        await ctx.respond("Please specify an amount between 1 and 100.", ephemeral=True)
        return
    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.respond(f"Deleted {len(deleted) - 1} messages.", ephemeral=True, delete_after=5)

@bot.slash_command(name="mute", description="Mute a user temporarily.")
@discord.default_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, duration: Optional[str] = None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(role, speak=False, send_messages=False, add_reactions=False)
    await member.add_roles(role)
    await ctx.respond(f"{member.mention} has been muted.")
    if duration:
        seconds = parse_duration(duration)
        if seconds:
            await asyncio.sleep(seconds)
            await member.remove_roles(role)
            await ctx.followup.send(f"{member.mention} has been unmuted after {duration}.")

@bot.slash_command(name="kick", description="Kick a user from the server.")
@discord.default_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, reason: Optional[str] = None):
    await member.kick(reason=reason)
    await ctx.respond(f"{member.mention} has been kicked. Reason: {reason or 'No reason provided.'}")

@bot.slash_command(name="ban", description="Ban a user from the server.")
@discord.default_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, reason: Optional[str] = None):
    await member.ban(reason=reason)
    await ctx.respond(f"{member.mention} has been banned. Reason: {reason or 'No reason provided.'}")

# Run bot
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN not set in env variables")
bot.run(DISCORD_TOKEN)
