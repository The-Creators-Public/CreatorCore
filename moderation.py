import discord
from discord.ext import commands
import asyncio
from typing import Optional

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def parse_duration(self, duration_str):
        import re
        match = re.match(r"(\\d+)([smhd])", duration_str.lower())
        if not match:
            return None
        amount, unit = match.groups()
        amount = int(amount)
        return {"s": 1, "m": 60, "h": 3600, "d": 86400}.get(unit, 0) * amount

    @commands.slash_command(name="mute", description="Mute a user temporarily.")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, duration: Optional[str] = None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(role, speak=False, send_messages=False, add_reactions=False)
        await member.add_roles(role)
        await ctx.respond(f"{member.mention} has been muted.")
        if duration:
            seconds = self.parse_duration(duration)
            if seconds:
                await asyncio.sleep(seconds)
                await member.remove_roles(role)
                await ctx.followup.send(f"{member.mention} has been unmuted after {duration}.")

    @commands.slash_command(name="kick", description="Kick a user from the server.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason: Optional[str] = None):
        await member.kick(reason=reason)
        await ctx.respond(f"{member.mention} has been kicked. Reason: {reason or 'No reason provided.'}")

    @commands.slash_command(name="ban", description="Ban a user from the server.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason: Optional[str] = None):
        await member.ban(reason=reason)
        await ctx.respond(f"{member.mention} has been banned. Reason: {reason or 'No reason provided.'}")

    @commands.slash_command(name="clear", description="Clear a number of messages.")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        if amount < 1 or amount > 100:
            await ctx.respond("Please specify an amount between 1 and 100.", ephemeral=True)
            return
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.respond(f"Deleted {len(deleted) - 1} messages.", ephemeral=True, delete_after=5)

def setup(bot):
    bot.add_cog(Moderation(bot))
