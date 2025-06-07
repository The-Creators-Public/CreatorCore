import discord
from discord.ext import commands
import os
import sys
from utils.decorators import requires_admin
from dotenv import load_dotenv

load_dotenv(r"C:\Users\angie\The Creators Public\creatorcore-bot\data\.env")

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DISCORD_ADMIN_IDS = os.getenv("DISCORD_ADMIN_IDS")
        self.EMERGENCY_CODE = os.getenv("EMERGENCY_CODE")

    def is_admin(self, user_id):
        admin_ids = []
        if isinstance(self.DISCORD_ADMIN_IDS, str):
            admin_ids = [int(uid.strip()) for uid in self.DISCORD_ADMIN_IDS.strip("[]").split(",")]
        elif isinstance(self.DISCORD_ADMIN_IDS, list):
            admin_ids = [int(uid) for uid in self.DISCORD_ADMIN_IDS]  # type: ignore
        return user_id in admin_ids

    @commands.command()
    @requires_admin()
    async def shutdown(self, ctx):
        if not self.is_admin(ctx.author.id):
            await ctx.send("You don't have permission to shut down the bot.")
            return
        await ctx.send("Shutting down...")
        await self.bot.close()

    @commands.command()
    @requires_admin()
    async def restart(self, ctx):
        if not self.is_admin(ctx.author.id):
            await ctx.send("You don't have permission to restart the bot.")
            return
        await ctx.send("Restarting...")
        try:
            await ctx.author.send("🔄 The bot is restarting. You'll be notified when it's back online.")
        except discord.Forbidden:
            print(f"Could not DM user {ctx.author.id}")
        await self.bot.close()
        os.execv(sys.executable, ['python'] + sys.argv)

    @commands.command()
    @requires_admin()
    async def say(self, ctx, *, message: str):
        if not self.is_admin(ctx.author.id):
            await ctx.send("You don't have permission to use this command.")
            return
        await ctx.send(message)

    @commands.command(name="override_shutdown")
    @requires_admin()
    async def override_shutdown(self, ctx, code: str):
        if code == self.EMERGENCY_CODE:
            await ctx.send("Emergency override accepted. Shutting down immediately.")
            await self.bot.close()
        else:
            await ctx.send("Invalid override code.")

def setup(bot):
    bot.add_cog(Admin(bot))
