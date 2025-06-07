import discord
from discord.ext import commands
from utils.helpers import text_to_speech, play_audio_in_voice
from utils.query_ollama import query_ollama
import io

class AIIntegration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="askcore", description="Use llama3.2 for coding questions or design help.")
    async def askcore(self, ctx, question: str):
        await ctx.defer()
        llm_response = await query_ollama(question)
        if llm_response.startswith("Error:"):
            await ctx.followup.send(llm_response)
            return
        audio_bytes = await text_to_speech(llm_response)
        if not audio_bytes:
            await ctx.followup.send("Error: Failed to generate speech audio.")
            return
        if ctx.author.voice and ctx.author.voice.channel:
            await play_audio_in_voice(ctx, audio_bytes, self.bot)
        else:
            audio_file = discord.File(io.BytesIO(audio_bytes), filename="response.mp3")
            await ctx.followup.send(content=llm_response, file=audio_file)

    @commands.slash_command(name="rewrite", description="Clean or optimize pasted code.")
    async def rewrite(self, ctx, code: str):
        # Placeholder implementation
        await ctx.respond(f"Rewritten code for:\n{code}")

    @commands.slash_command(name="idea", description="Generate mod ideas, biome names, mob types, etc.")
    async def idea(self, ctx):
        # Placeholder implementation
        await ctx.respond("Here is a mod idea: A biome with floating islands and unique mobs.")

def setup(bot):
    bot.add_cog(AIIntegration(bot))
