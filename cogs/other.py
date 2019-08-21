import asyncio
import datetime
import discord
from discord.ext import commands
import json

class other(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.errorcolor = 0xFF2B2B
        self.blurple = 0x7289DA

    @commands.command()
    @command.has_permissions(manage_guild = True)
    async def prefix(self, ctx, *, pre):
        if ctx.message.author.id == ctx.guild.owner.id:
            with open(r"PATHHERE\WumpusMod\prefixes.json", "r") as f:
                prefixes = json.load(f)

            prefixes[str(ctx.guild.id)] = pre
            embed = discord.Embed(
                title = "Prefix",
                description = f"{ctx.message.guild}'s prefix is  now `{pre}`",
                color = self.blurple
            )
            await ctx.send(embed = embed)

             with open(r"PATHHERE\WumpusMod\prefixes.json", "w") as f:
                json.dump(prefixes, f, indent = 4)

    @prefix.error()
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "You are missing the **Manage Server** permission!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)
            await ctx.message.delete()

    #Ping command
    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(
            title = f"Pong!",
            description = f"{round(self.bot.latency * 1000)} ms",
            color = self.blurple
        )
        await ctx.send(embed = embed)

    #Github command
    @commands.command()
    async def github(self, ctx):
        embed = discord.Embed(
            title = f"Feel free to check out the github!",
            url = "https://github.com/xPolar/WumpusMod",
            color = self.blurple
        )
        await ctx.send(embed = embed)

    #Support command
    @commands.command()
    async def support(self, ctx):
        embed = discord.Embed(
            title = f"Feel free to join our support server!",
            url = "https://discord.gg/gkAKatd",
            color = self.blurple
        )
        await ctx.send(embed = embed)

    #Invite command
    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(
            title = f"Feel free to invite me!",
            url = "https://discordapp.com/api/oauth2/authorize?client_id=596532744218214402&permissions=8&scope=bot",
            color = self.blurple
        )
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(other(bot))
