import discord
from discord.ext import commands
import json
from typing import Optional
import os
import aiohttp

class Modding(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mods = []
        self.resources = {}
        try:
            with open(os.path.join("data", "mods.json"), "r") as f:
                self.mods = json.load(f)
        except Exception:
            self.mods = []
        try:
            with open(os.path.join("data", "resources.json"), "r") as f:
                self.resources = json.load(f)
        except Exception:
            self.resources = {}

    @commands.slash_command(name="modlist", description="Show current mods with links and authors.")
    async def modlist(self, ctx):
        # Fetch popular mods from Modrinth API
        url = "https://api.modrinth.com/v2/project?facets=%5B%5B%22category%3Amods%22%5D%5D&index=0&limit=10"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    hits = data.get("hits", [])
                    if hits:
                        mod_names = [mod.get("title", "Unknown") for mod in hits]
                        await ctx.respond(", ".join(mod_names))
                        return
        # Fallback to static data
        mod_names = [mod.get("name", "Unknown") for mod in self.mods]
        await ctx.respond(", ".join(mod_names) if mod_names else "No mods available.")

    @commands.slash_command(name="showcase", description="Display details, images, or status of a selected mod.")
    async def showcase(self, ctx, mod: str):
        # Search mod by name using Modrinth API
        search_url = f"https://api.modrinth.com/v2/search?query={mod}&facets=%5B%5B%22category%3Amods%22%5D%5D&limit=1"
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    hits = data.get("hits", [])
                    if hits:
                        mod_info = hits[0]
                        title = mod_info.get("title", "Unknown")
                        author = mod_info.get("author", "Unknown")
                        description = mod_info.get("description", "No description")
                        project_id = mod_info.get("project_id", "")
                        mod_link = f"https://modrinth.com/mod/{project_id}" if project_id else "No link"
                        await ctx.respond(f"Mod: {title}\nAuthor: {author}\nDescription: {description}\nLink: {mod_link}")
                        return
        # Fallback to static data
        mod_info = next((m for m in self.mods if m.get("name", "").lower() == mod.lower()), None)
        if mod_info:
            await ctx.respond(f"Mod: {mod_info.get('name')}\nAuthor: {mod_info.get('author')}\nDescription: {mod_info.get('description', 'No description')}\nLink: {mod_info.get('link', 'No link')}")
        else:
            await ctx.respond(f"No mod found with name '{mod}'.")

    @commands.slash_command(name="craft", description="Return crafting recipes from Minecraft Recipes API.")
    async def craft(self, ctx, item: str):
        url = f"https://mc-recp.tobycm.dev/api/recipes/{item.lower()}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    ingredients = data.get("ingredients", [])
                    if ingredients:
                        ingredients_list = ", ".join(ingredients)
                        await ctx.respond(f"Crafting recipe for {item}: {ingredients_list}")
                    else:
                        await ctx.respond(f"No ingredients found for {item}.")
                else:
                    await ctx.respond(f"No crafting recipe found for {item}.")

    @commands.slash_command(name="weather", description="Simulate biome conditions.")
    async def weather(self, ctx, biome: str):
        description = self.resources.get("biomes", {}).get(biome.lower())
        if description:
            await ctx.respond(f"Weather simulation for biome '{biome}': {description}")
        else:
            await ctx.respond(f"No weather simulation available for biome '{biome}'.")

    @commands.slash_command(name="buildhelp", description="Link to tutorials, code snippets, or give tips.")
    async def buildhelp(self, ctx, topic: str):
        tutorial_link = self.resources.get("tutorials", {}).get(topic.lower())
        if tutorial_link:
            await ctx.respond(f"Build help for topic '{topic}': {tutorial_link}")
        else:
            await ctx.respond(f"No build help available for topic '{topic}'.")

def setup(bot):
    bot.add_cog(Modding(bot))
