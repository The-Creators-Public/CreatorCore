import discord
from discord.ext import commands
from typing import Optional

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ping", description="Check the bot's latency.")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        await ctx.respond(f"Pong! Latency: {latency}ms")

    @commands.slash_command(name="userinfo", description="Get info about a user.")
    async def userinfo(self, ctx, member: Optional[discord.Member] = None):
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

    @commands.slash_command(name="serverinfo", description="Display server information.")
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f"{guild.name}", description=guild.description or "No description", color=discord.Color.blue())
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="Owner", value=str(guild.owner))
        embed.add_field(name="Members", value=guild.member_count)
        embed.add_field(name="Roles", value=str(len(guild.roles)))
        embed.add_field(name="Channels", value=str(len(guild.channels)))
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))
