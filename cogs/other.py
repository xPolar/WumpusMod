import discord
from discord.ext import commands
import json

class other(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.errorcolor = 0xFF2B2B
        self.blurple = 0x7289DA
    async def is_guild_owner(ctx):
        return ctx.author.id == ctx.guild.owner.id

    @commands.command()
    @command.has_permissions(manage_guild = True)
    async def prefix(self, ctx, *, pre):
        if ctx.message.author.id == ctx.guild.owner.id:
            with open(r"DIRECTERYPATHHERE\prefixes.json", "r") as f:
                prefixes = json.load(f)

            prefixes[str(ctx.guild.id)] = pre
            embed = discord.Embed(
                title = "Prefix",
                description = f"{ctx.message.guild}'s prefix is  now `{pre}`",
                color = self.blurple
            )
            await ctx.send(embed = embed)

            with open(r"DIRECTERYPATHHERE\prefixes.json", "w") as f:
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

    @commands.command()
    async def help(self, ctx, module = None):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefix = prefixes[str(ctx.message.guild.id)]
        if module == None:
            embed = discord.Embed(
                title = "``Moderation``",
                description = "6 total commands.",
                color = self.blurple
            )
            embed.set_author(name = "Categorys")
            embed.add_field(name = "``Tickets``", value = "5 total commands.")
            embed.add_field(name = "``Other``", value = "7 total commands.")
            embed.set_footer(text = f"For more information on each category do {prefix}help (Category).")
            await ctx.send(embed = embed)
        else:
            if module.lower() == "moderation":
                embed = discord.Embed(
                    title = "Commands",
                    description = "**Purge / Clear** - Deletes a large amount of messages.\n**Kick** - Kicks a user from the server.\n**Ban** - Bans a user from the server.\n**Unban** - Unbans a user from the server.\n**Mute** - Mutes a user so they can't talk\n**Unmute** - Unmutes a user so they can talk.",
                    color = self.blurple
                )
                embed.set_author(name = "Moderation")
                embed.set_footer(text = f"For more information on each command do {prefix}help (Command).")
                await ctx.send(embed = embed)
            elif module.lower() == "tickets":
                embed = discord.Embed(
                    title = "Commands",
                    description = "**Ticket** - Creates a new ticket.\n**Adduser** - Adds a user to a ticket.\n**Removeuser / Rmuser** - Removes a user from a ticket.\n**Close** - Closes a ticket.\n**Supporteradd** - Adds a user to the supporter role.",
                    color = self.blurple
                )
                embed.set_author(name = "Tickets")
                embed.set_footer(text = f"For more information on each command do {prefix}help (Command).")
                await ctx.send(embed = embed)
            elif module.lower() == "other":
                embed = discord.Embed(
                    title = "Commands",
                    description = "**Ping** - Shows the bot's current ping.\n**Information / Info** - Shows some basic information about the bot.\n**Info** - Shows some basic information.\n**Invite** - Sends a link to invite the bot.\n**Support** - Sends a link to join the support server.\n**Github** - Sends a link to view the github.\n**Leave** - Makes the bot leave the server so you don't have to kick it.",
                    color = self.blurple
                )
                embed.set_author(name = "Tickets")
                embed.set_footer(text = f"For more information on each command do {prefix}help (Command).")
                await ctx.send(embed = embed)
            elif module.lower() == "purge" or module.lower() == "clear":
                embed = discord.Embed(
                    title = "Description",
                    description = "Removes a large amount of messages in a channel.",
                    color = self.blurple
                )
                embed.set_author(name = "Purge / Clear")
                embed.add_field(name = "Usage", value = f"``{prefix}purge (Amount)``\n``{prefix}clear (Amount)``")
                await ctx.send(embed = embed)
            elif module.lower() == "kick":
                embed = discord.Embed(
                    title = "Description",
                    description = "Kicks a user from the server.",
                    color = self.blurple
                )
                embed.set_author(name = "Kick")
                embed.add_field(name = "Usage", value = f"``{prefix}kick (User) (Reason)``")
                await ctx.send(embed = embed)
            elif module.lower() == "ban":
                embed = discord.Embed(
                    title = "Description",
                    description = "Bans a user from the server.",
                    color = self.blurple
                )
                embed.set_author(name = "Ban")
                embed.add_field(name = "Usage", value = f"``{prefix}ban (User) (Reason)``")
                await ctx.send(embed = embed)
            elif module.lower() == "unban":
                embed = discord.Embed(
                    title = "Description",
                    description = "Unbans a user from the server.",
                    color = self.blurple
                )
                embed.set_author(name = "Unban")
                embed.add_field(name = "Usage", value = f"``{prefix}unban (User)``")
                await ctx.send(embed = embed)
            elif module.lower() == "mute":
                embed = discord.Embed(
                    title = "Description",
                    description = "Mutes a user so they can't talk.",
                    color = self.blurple
                )
                embed.set_author(name = "Mute")
                embed.add_field(name = "Usage", value = f"``{prefix}mute (User) (Reason)``")
                await ctx.send(embed = embed)
            elif module.lower() == "unmute":
                embed = discord.Embed(
                    title = "Description",
                    description = "Unmutes a user so they can talk.",
                    color = self.blurple
                )
                embed.set_author(name = "Unmute")
                embed.add_field(name = "Usage", value = f"``{prefix}unmute (User)``")
                await ctx.send(embed = embed)
            elif module.lower() == "ticket":
                embed = discord.Embed(
                    title = "Description",
                    description = "Creates a new ticket.",
                    color = self.blurple
                )
                embed.set_author(name = "Ticket")
                embed.add_field(name = "Usage", value = f"``{prefix}ticket (Reason)``")
                await ctx.send(embed = embed)
            elif module.lower() == "close":
                embed = discord.Embed(
                    title = "Description",
                    description = "Closes a ticket.",
                    color = self.blurple
                )
                embed.set_author(name = "Close")
                embed.add_field(name = "Usage", value = f"``{prefix}close``")
                await ctx.send(embed = embed)
            elif module.lower() == "adduser":
                embed = discord.Embed(
                    title = "Description",
                    description = "Adds a user to a ticket.",
                    color = self.blurple
                )
                embed.set_author(name = "Adduser")
                embed.add_field(name = "Usage", value = f"``{prefix}adduser (User)``")
                await ctx.send(embed = embed)
            elif module.lower() == "removeuser" or module.lower() == "rmuser":
                embed = discord.Embed(
                    title = "Description",
                    description = "Removes a user from a ticket.",
                    color = self.blurple
                )
                embed.set_author(name = "Removeuser / Rmuser")
                embed.add_field(name = "Usage", value = f"``{prefix}removemuser (User)``\n``{prefix}rmuser (User)``")
                await ctx.send(embed = embed)
            elif module.lower() == "supporteradd":
                embed = discord.Embed(
                    title = "Description",
                    description = "Adds a user to the supporter role.",
                    color = self.blurple
                )
                embed.set_author(name = "Supporteradd")
                embed.add_field(name = "Usage", value = f"``{prefix}supporteradd (User)``")
                await ctx.send(embed = embed)
            elif module.lower() == "ping":
                embed = discord.Embed(
                    title = "Description",
                    description = "Shows the bot's current ping.",
                    color = self.blurple
                )
                embed.set_author(name = "Ping")
                await ctx.send(embed = embed)
            elif module.lower() == "info" or module.lower() == "information":
                embed = discord.Embed(
                    title = "Description",
                    description = "Shows some basic information.",
                    color = self.blurple
                )
                embed.set_author(name = "Info / Information")
                await ctx.send(embed = embed)
            elif module.lower() == "invite":
                embed = discord.Embed(
                    title = "Description",
                    description = "Sends a link to invite the bot.",
                    color = self.blurple
                )
                embed.set_author(name = "Invite")
                await ctx.send(embed = embed)
            elif module.lower() == "support":
                embed = discord.Embed(
                    title = "Description",
                    description = "Shows a link to join the support server.",
                    color = self.blurple
                )
                embed.set_author(name = "Support")
                await ctx.send(embed = embed)
            elif module.lower() == "github":
                embed = discord.Embed(
                    title = "Description",
                    description = "Sends a link to view the github.",
                    color = self.blurple
                )
                embed.set_author(name = "Github")
                await ctx.send(embed = embed)
            elif module.lower() == "leave":
                embed = discord.Embed(
                    title = "Description",
                    description = "Leaves the server so you don't have to kick it.",
                    color = self.blurple
                )
                embed.set_author(name = "Leave")
                await ctx.send(embed = embed)
            elif module.lower() == "prefix":
                embed = discord.Embed(
                    title = "Description",
                    description = "Set the server's prefix",
                    color = self.blurple
                )
                embed.set_author(name = "Prefix")
                ctx.send(embed = embed)
            else:
                embed = discord.Embed(
                    title = "Help Error",
                    description = f"{module} is not a category/command!",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed)

    #Ping command
    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(
            title = f"Pong! {round(self.bot.latency * 1000)} ms",
            color = self.blurple
        )
        await ctx.send(embed = embed)

    #Invite command
    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(
            title = "Invite Link",
            description = "Feel free to invite me!",
            url = "https://discordapp.com/oauth2/authorize?client_id=596532744218214402&permissions=8&scope=bot",
            color = self.blurple
        )
        await ctx.send(embed = embed)

    #Support command
    @commands.command()
    async def support(self, ctx):
        embed = discord.Embed(
            title = "Support Server",
            description = "Feel free to join the support server!",
            url = "https://discordapp.com/invite/tjA5ssJ",
            color = self.blurple
        )
        await ctx.send(embed = embed)

    #Info command
    @commands.command(aliaes = ["information"])
    async def info(self, ctx):
        embed = discord.Embed(
            title = "Developer",
            description = "This bot was made by <@229695200082132993>.",
            color = self.blurple
        )
        embed.set_author(name = "Information")
        embed.add_field(name = "Uses", value = "WumpusMod is a moderation and ticket bot.")
        embed.add_field(name = "Libary", value = "<:python:596577462335307777> Discord.py")
        embed.add_field(name = "Important Links", value = "[Invite Link](https://discordapp.com/oauth2/authorize?client_id=596532744218214402&permissions=8&scope=bot), [Support Server](https://discordapp.com/invite/tjA5ssJ), and [Github](https://github.com/xPolar/WumpusMod)", inline = False)
        embed.add_field(name = "Prefix", value = f"`{prefix}`")
        embed.add_field(name = "Server Count", value = f"{len(self.bot.guilds)}")
        embed.add_field(name = "User Count", value = f"{len(self.bot.users)}")
        await ctx.send(embed = embed)

    #Leave command
    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def leave(self, ctx):
        embed = discord.Embed(
            title = "Leave",
            description = "I have left this server, please let the devs know why you wanted to remove the bot by joining the [Support Server](https://discordapp.com/invite/tjA5ssJ).",
            color = self.errorcolor
        )
        await ctx.send(embed = embed)
        await ctx.guild.leave()

    @leave.error
    async def leave_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "You are missing the **Manage Server** permission!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
            await ctx.message.delete()

    #Github command
    @commands.command()
    async def github(self, ctx):
        embed = discord.Embed(
            title = "Github",
            description = "Feel free to check out the github!",
            url = "https://github.com/xPolar/WumpusMod",
            color = self.blurple
        )
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(other(bot))

