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
    async def help(self, ctx):
        with open(r"PATHHERE\WumpusMod\Data\prefixes.json", "r") as f:
            prefixes = json.load(f)
        if str(ctx.message.guild.id) not in prefixes:
            prefix = "w!"
        else:
            prefix = prefixes[str(ctx.message.guild.id)]
        channel = ctx.message.channel
        key = discord.Embed(
            title = "Key",
            description = ":one: - View all **moderation** commands.\n:two: - View all **ticket system** commands.\n:three: - View all **other** commands.\n⏹ - Stop help message.",
            timestamp = datetime.datetime.utcnow(),
            color = self.blurple
        )
        key.set_author(name = "Help")
        key.set_footer(text = f"For more help join the support server with {prefix}support!")
        page_1 = discord.Embed(
            title = "Commands",
            description = "**Purge / Clear** - Deletes a large amount of messages.\n**Kick** - Kicks a member from the server.\n**Ban** - Bans a user from the server.\n**Unban** - Removes a user's ban.\**Mute** - Mutes a user so they can't talk.\n**Unmute** - Unmutes a user so they can talk.\n**Nuke** - Delete all messages in a channel.",
            timestamp = datetime.datetime.utcnow(),
            color = self.blurple
        )
        page_1.set_author(name = "Moderation")
        page_1.set_footer(text = f"For more info on each command do {prefix}help (Command)")
        page_2 = discord.Embed(
            title = "Commands",
            description = "**Ticket** - Create a new ticket.\n**Close** - Close a ticket.\n**Adduser / Useradd** - Add a user to the ticket.\n**Removeuser / Userremove** - Remove a user from a ticket.",
            timestamp = datetime.datetime.utcnow(),
            color = self.blurple
        )
        page_2.set_author(name = "Ticket System")
        page_2.set_footer(text = f"For more info on each command do {prefix}help (Command)")
        page_3 = discord.Embed(
            title = "Commands",
            description = "**Help** - This command.\n**Support** - Get an invite link to the Wumpus Developments Discord server.\n**Invite** - Get an invite link to invite WumpusMod.\n**Website** - Get the link for the Wumpus Developments website.\n**Github** - Get the link for the WumpusMod github.\n**Prefix** - Set the prefix for your server.",
            timestamp = datetime.datetime.utcnow(),
            color = self.blurple
        )
        page_2.set_author(name = "Other")
        page_2.set_footer(text = f"For more info on each command do {prefix}help (Command)")
        msg = await ctx.send(embed = key)

        def check(reaction, user):
            return str(reaction.emoji) == ":one:" or str(reaction.emoji) == ":two:" or str(reaction.emoji) == ":three:" or str(reaction.emoji) == "⏹"

        async def wait_for():
            try:
                await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await msg.delete()
            else:
                if str(reaction.emoji) == ":one:":
                    await msg.edit(embed = page_1)
                elif str(reaction.emoji) == ":two:":
                    await msg.edit(embed = page_2)
                elif str(reaction.emoji) == ":three:":
                    await msg.edit(embed = page_3)
                elif str(reaction.emoji) == "⏹":
                    await msg.edit(embed = key)
                wait_for()
        wait_for()

def setup(bot):
    bot.add_cog(other(bot))
