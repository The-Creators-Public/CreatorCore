import discord
from discord.ext import commands
import aiohttp
import random
import re

class DnD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_base = "https://www.dnd5eapi.co/api"

    @commands.slash_command(name="roll", description="Roll dice with standard notation, e.g. 1d20+5")
    async def roll(self, ctx, dice: str):
        pattern = r"(\d*)d(\d+)([+-]\d+)?"
        match = re.fullmatch(pattern, dice.replace(" ", ""))
        if not match:
            await ctx.respond("Invalid dice notation. Use NdM+X format, e.g. 1d20+5")
            return
        num_dice = int(match.group(1)) if match.group(1) else 1
        dice_sides = int(match.group(2))
        modifier = int(match.group(3)) if match.group(3) else 0

        rolls = [random.randint(1, dice_sides) for _ in range(num_dice)]
        total = sum(rolls) + modifier
        rolls_str = ", ".join(str(r) for r in rolls)
        mod_str = f" {modifier:+d}" if modifier else ""
        await ctx.respond(f"Rolls: [{rolls_str}]{mod_str} = **{total}**")

    @commands.slash_command(name="spell", description="Lookup a spell by name")
    async def spell(self, ctx, name: str):
        async with aiohttp.ClientSession() as session:
            # Get spell index from name
            async with session.get(f"{self.api_base}/spells") as resp:
                if resp.status != 200:
                    await ctx.respond("Failed to fetch spells list.")
                    return
                data = await resp.json()
                spells = data.get("results", [])
                spell_index = None
                for spell in spells:
                    if spell["name"].lower() == name.lower():
                        spell_index = spell["index"]
                        break
                if not spell_index:
                    await ctx.respond(f"Spell '{name}' not found.")
                    return
            # Get spell details
            async with session.get(f"{self.api_base}/spells/{spell_index}") as resp:
                if resp.status != 200:
                    await ctx.respond(f"Failed to fetch details for spell '{name}'.")
                    return
                spell_data = await resp.json()
                desc = spell_data.get("desc", ["No description available."])
                level = spell_data.get("level", "Unknown")
                school = spell_data.get("school", {}).get("name", "Unknown")
                components = ", ".join(spell_data.get("components", []))
                material = spell_data.get("material", "")
                if material:
                    components += f" (Material: {material})"
                embed = discord.Embed(title=spell_data.get("name", "Spell"), description="\n".join(desc), color=discord.Color.blue())
                embed.add_field(name="Level", value=str(level))
                embed.add_field(name="School", value=school)
                embed.add_field(name="Components", value=components)
                await ctx.respond(embed=embed)

    @commands.slash_command(name="character_create", description="Create a basic D&D character")
    async def character_create(self, ctx, name: str, race: str, char_class: str):
        # Basic placeholder implementation
        await ctx.respond(f"Character created: {name}, Race: {race}, Class: {char_class}")

    @commands.slash_command(name="campaign", description="Manage your D&D campaign (placeholder)")
    async def campaign(self, ctx, action: str, *, details: str = ""):
        await ctx.respond(f"Campaign command received. Action: {action}, Details: {details or 'None'}")

def setup(bot):
    bot.add_cog(DnD(bot))
