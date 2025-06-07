import discord
from discord.ext import commands

class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="docs", description="Link to official docs, GitHub wiki, or tutorials.")
    async def docs(self, ctx):
        await ctx.respond("Here is the official documentation: https://github.com/yourrepo/docs")

    @commands.slash_command(name="issues", description="Redirect users to GitHub Issues with instructions.")
    async def issues(self, ctx):
        await ctx.respond("Report issues here: https://github.com/yourrepo/issues")

    @commands.slash_command(name="request", description="Log a mod feature request or improvement.")
    async def request(self, ctx, feature: str):
        # Here you might log the request to a file or channel
        await ctx.respond(f"Feature request received: {feature}")

    @commands.slash_command(name="roadmap", description="Show the development roadmap.")
    async def roadmap(self, ctx):
        await ctx.respond("Development roadmap: https://github.com/yourrepo/projects")

def setup(bot):
    bot.add_cog(Developer(bot))
