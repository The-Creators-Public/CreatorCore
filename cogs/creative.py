import discord
from discord.ext import commands

class Creative(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="inspire", description="Generate motivational quotes or design ideas.")
    async def inspire(self, ctx):
        await ctx.respond("Stay creative! Here's a motivational quote: 'Creativity is intelligence having fun.' - Albert Einstein")

    @commands.slash_command(name="cat", description="Show a random cat picture.")
    async def cat(self, ctx):
        await ctx.respond("Here's a cute cat picture! 🐱 (Image URL or API integration pending)")

    @commands.slash_command(name="dog", description="Show a random dog picture.")
    async def dog(self, ctx):
        await ctx.respond("Here's a cute dog picture! 🐶 (Image URL or API integration pending)")

    @commands.slash_command(name="mcjoke", description="Tell a Minecraft joke.")
    async def mcjoke(self, ctx):
        await ctx.respond("Why did the creeper cross the road? To get to the other ssssside!")

    @commands.slash_command(name="daily", description="Give a daily creative challenge or trivia.")
    async def daily(self, ctx):
        await ctx.respond("Today's creative challenge: Build a treehouse using only natural materials!")

def setup(bot):
    bot.add_cog(Creative(bot))
