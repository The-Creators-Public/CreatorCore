import discord
from discord.ext import commands
from typing import Optional
import asyncio
import sqlite3
import re
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv

load_dotenv(r"C:\Users\angie\The Creators Public\creatorcore-bot\data\.env")

class Community(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect(r"C:\Users\angie\The Creators Public\creatorcore-bot\data\reminders.db")
        self.create_tables()
        self.bot.loop.create_task(self.reminder_loop())

    def create_tables(self):
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                channel_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                remind_at TEXT NOT NULL,
                recurring_interval INTEGER,
                timezone TEXT,
                active INTEGER DEFAULT 1
            )
        """)
        self.db.commit()

    async def reminder_loop(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            now = datetime.utcnow()
            cursor = self.db.cursor()
            cursor.execute("SELECT id, user_id, channel_id, message, remind_at, recurring_interval, timezone FROM reminders WHERE active=1")
            reminders = cursor.fetchall()
            for reminder in reminders:
                id_, user_id, channel_id, message, remind_at_str, recurring_interval, timezone = reminder
                remind_at = datetime.fromisoformat(remind_at_str)
                if timezone:
                    tz = pytz.timezone(timezone)
                    remind_at = tz.localize(remind_at).astimezone(pytz.utc).replace(tzinfo=None)
                if remind_at <= now:
                    channel = self.bot.get_channel(channel_id)
                    user = self.bot.get_user(user_id)
                    if channel and user:
                        try:
                            await user.send(f"⏰ Reminder: {message}")
                        except:
                            await channel.send(f"{user.mention} ⏰ Reminder: {message}")
                    if recurring_interval:
                        next_remind = remind_at + timedelta(seconds=recurring_interval)
                        cursor.execute("UPDATE reminders SET remind_at=? WHERE id=?", (next_remind.isoformat(), id_))
                    else:
                        cursor.execute("UPDATE reminders SET active=0 WHERE id=?", (id_,))
                    self.db.commit()
            await asyncio.sleep(60)

    def parse_duration(self, duration_str):
        match = re.match(r"(\d+)([smhd])", duration_str.lower())
        if not match:
            return None
        amount, unit = match.groups()
        amount = int(amount)
        return {"s": 1, "m": 60, "h": 3600, "d": 86400}.get(unit, 0) * amount

    @commands.slash_command(name="event", description="Show upcoming events, contests, or build jams.")
    async def event(self, ctx):
        await ctx.respond("")

    @commands.slash_command(name="poll", description="Create a simple poll.")
    async def poll(self, ctx, question: str, *options: str):
        if len(options) < 2:
            await ctx.respond("Please provide at least two options for the poll.")
            return
        if len(options) > 10:
            await ctx.respond("You can provide up to 10 options.")
            return

        embed = discord.Embed(title="Poll", description=question, color=discord.Color.blue())
        for i, option in enumerate(options, start=1):
            embed.add_field(name=f"Option {i}", value=option, inline=False)

        message = await ctx.respond(embed=embed)
        # Store votes in memory for simplicity; for persistence, use DB
        self.votes = {}
        self.poll_message = await message.original_message()

        for i in range(len(options)):
            await self.poll_message.add_reaction(chr(0x1F1E6 + i))  # Regional indicator symbols 🇦 🇧 🇨 ...

    @commands.slash_command(name="remindme", description="Set a custom reminder.")
    async def remindme(self, ctx, time: str, *, message: str):
        seconds = self.parse_duration(time)
        if seconds is None:
            await ctx.respond("Invalid time format. Use formats like 10m, 2h, 1d.")
            return
        remind_at = datetime.utcnow() + timedelta(seconds=seconds)
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO reminders (user_id, channel_id, message, remind_at) VALUES (?, ?, ?, ?)",
            (ctx.author.id, ctx.channel.id, message, remind_at.isoformat())
        )
        self.db.commit()
        await ctx.respond(f"Reminder set for {time}: {message}")

    @commands.slash_command(name="profile", description="Show a user's mod contributions and roles.")
    async def profile(self, ctx, user: Optional[discord.Member] = None):
        user = user or ctx.author
        # TODO: Fetch and display mod contributions and roles from database or API
        await ctx.respond(f"Profile for {user.display_name} (mod contributions and roles).")

    @commands.slash_command(name="suggest", description="Log a suggestion to the mod channel or file.")
    async def suggest(self, ctx, idea: str):
        # TODO: Log suggestion to mod channel or file
        await ctx.respond(f"Suggestion received: {idea}")

    @commands.slash_command(name="rank", description="Show user leveling or creative badges.")
    async def rank(self, ctx, user: Optional[discord.Member] = None):
        user = user or ctx.author
        # TODO: Implement XP system and badge display
        await ctx.respond(f"{user.display_name}'s rank and badges (XP system pending).")

def setup(bot):
    bot.add_cog(Community(bot))
