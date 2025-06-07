import discord
from discord.ext import commands
import os
import aiohttp
from datetime import datetime
from typing import Optional, List

GITHUB_API_URL = "https://api.github.com"

class GitHubStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.github_token = os.getenv("GITHUB_TOKEN")
        if not self.github_token:
            print("Warning: GITHUB_TOKEN not set in environment variables.")

    @commands.slash_command(name="stats", description="Get GitHub repository statistics.")
    async def githubstats(
        self,
        ctx: discord.ApplicationContext,
        repos: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ):
        """
        repos: Comma-separated list of repository names (owner/repo)
        start_date, end_date: Optional ISO format dates (YYYY-MM-DD)
        """
        await ctx.defer()

        repo_list = [r.strip() for r in repos.split(",") if r.strip()]
        if not repo_list:
            await ctx.respond("Please provide at least one repository name in the format owner/repo.")
            return

        headers = {
            "Authorization": f"token {self.github_token}"
        } if self.github_token else {}

        # Validate dates
        start_dt = None
        end_dt = None
        try:
            if start_date:
                start_dt = datetime.fromisoformat(start_date)
            if end_date:
                end_dt = datetime.fromisoformat(end_date)
        except ValueError:
            await ctx.respond("Invalid date format. Please use YYYY-MM-DD.")
            return

        embed = discord.Embed(title="GitHub Repository Statistics", color=discord.Color.blue())

        async with aiohttp.ClientSession() as session:
            for repo in repo_list:
                repo_url = f"{GITHUB_API_URL}/repos/{repo}"
                async with session.get(repo_url, headers=headers) as resp:
                    if resp.status == 404:
                        embed.add_field(name=repo, value="Repository not found or invalid name.", inline=False)
                        continue
                    elif resp.status != 200:
                        embed.add_field(name=repo, value=f"Error fetching data: HTTP {resp.status}", inline=False)
                        continue
                    repo_data = await resp.json()

                # Fetch commits count with optional date filtering
                commits_url = f"{GITHUB_API_URL}/repos/{repo}/commits"
                params = {}
                if start_date:
                    params["since"] = start_date + "T00:00:00Z"
                if end_date:
                    params["until"] = end_date + "T23:59:59Z"

                commits_count = 0
                page = 1
                per_page = 100
                while True:
                    params.update({"per_page": per_page, "page": page})
                    async with session.get(commits_url, headers=headers, params=params) as resp:
                        if resp.status != 200:
                            break
                        commits = await resp.json()
                        if not commits:
                            break
                        commits_count += len(commits)
                        if len(commits) < per_page:
                            break
                        page += 1

                # Fetch pull requests count with optional date filtering
                pulls_url = f"{GITHUB_API_URL}/repos/{repo}/pulls"
                pulls_count = 0
                page = 1
                while True:
                    params_pulls = {"state": "all", "per_page": per_page, "page": page}
                    async with session.get(pulls_url, headers=headers, params=params_pulls) as resp:
                        if resp.status != 200:
                            break
                        pulls = await resp.json()
                        if not pulls:
                            break
                        # Filter by date if specified
                        if start_dt or end_dt:
                            filtered_pulls = []
                            for pr in pulls:
                                created_at = datetime.fromisoformat(pr["created_at"].replace("Z", "+00:00"))
                                if start_dt and created_at < start_dt:
                                    continue
                                if end_dt and created_at > end_dt:
                                    continue
                                filtered_pulls.append(pr)
                            pulls_count += len(filtered_pulls)
                        else:
                            pulls_count += len(pulls)
                        if len(pulls) < per_page:
                            break
                        page += 1

                description = (
                    f"**Stars:** {repo_data.get('stargazers_count', 'N/A')}\n"
                    f"**Forks:** {repo_data.get('forks_count', 'N/A')}\n"
                    f"**Open Issues:** {repo_data.get('open_issues_count', 'N/A')}\n"
                    f"**Commits:** {commits_count}\n"
                    f"**Pull Requests:** {pulls_count}\n"
                    f"**Default Branch:** {repo_data.get('default_branch', 'N/A')}\n"
                    f"[Repository Link]({repo_data.get('html_url', '')})"
                )
                embed.add_field(name=repo, value=description, inline=False)

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(GitHubStats(bot))
