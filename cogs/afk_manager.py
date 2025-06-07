import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv(r"C:\Users\angie\The Creators Public\creatorcore-bot\data\.env")

class AFKManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_channel_id = int(os.getenv("AFK_CHANNEL_ID", 0))  # Set your AFK channel ID in .env

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # If user is not in a voice channel, ignore
        if after.channel is None:
            return

        # If user is already in AFK channel, ignore
        if after.channel.id == self.afk_channel_id:
            return

        # Check if user is muted or deafened (could be considered AFK)
        if after.self_deaf or after.self_mute or after.deaf or after.mute:
            afk_channel = self.bot.get_channel(self.afk_channel_id)
            if afk_channel is not None:
                try:
                    await member.move_to(afk_channel)
                except discord.Forbidden:
                    print(f"Permission denied to move {member} to AFK channel.")
                except Exception as e:
                    print(f"Error moving {member} to AFK channel: {e}")

def setup(bot):
    bot.add_cog(AFKManager(bot))
