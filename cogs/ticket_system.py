import asyncio
import datetime
import discord
from discord.ext import commands
import json

class ticket_system(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.errorcolor = 0xFF2B2B
        self.blurple = 0x7289DA

    @commands.command()
    @commands.cooldown(rate = 1, per = 60, type = commands.BucketType.member)
    async def ticket(self, ctx, *, reason = None):
        """
        Create a ticket.
        """
        try:
            with open(r"PATHHERE\WumpusMod\Data\prefixes.json", "r") as f:
                prefixes = json.load(f)
            if str(ctx.message.guild.id) not in prefixes:
                prefix = "w!"
            else:
                prefix = prefixes[str(ctx.message.guild.id)]
            with open(r"PATHHERE\WumpusMod\Data\supportroles.json", "r") as f:
                supportroles = json.load(f)
            with open(r"PATHHERE\WumpusMod\Data\ticketcategorys.json", "r") as f:
                ticketcategorys = json.load(f)
            with open(r"PATHHERE\WumpusMod\Data\mentions.json", "r") as f:
                mentions = json.load(f)
            with open(r"PATHHERE\WumpusMod\Data\ticketlogchannels.json", "r") as f:
                ticketlogchannels = json.load(f)
            if str(ctx.message.guild.id) not in supportroles:
                embed = discord.Embed(
                    title = "Ticket Error",
                    description = "This server has no support role set!",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed)
            else:
                supportrole  = supportroles[str(ctx.message.guild.id)]
                if str(ctx.message.guild.id) not in ticketcategorys:
                    embed = discord.Embed(
                        title = "Ticket Error",
                        description = "This server has no ticket category set!",
                        color = self.errorcolor
                    )
                    await ctx.send(embed = embed)
                else:
                    ticketcategory = ticketcategorys[str(ctx.message.guild.id)]
                    supporter = discord.utils.get(ctx.guild.roles, id = supportrole)
                    overwrites = {
                        ctx.guild.default_role: discord.PermissionOverwrite(read_messages = False),
                        ctx.author: discord.PermissionOverwrite(read_messages = True),
                        self.bot.user: discord.PermissionOverwrite(read_messages = True),
                        supporter: discord.PermissionOverwrite(read_messages = True),
                    }
                    ticketcategory = discord.utils.get(ctx.guild.categories, id = ticketcategory)
                    ticketname = f"{ctx.message.author.name}-{ctx.message.author.discriminator}"
                    ticketalreadymade = False
                    for text_channel in ticketcategory.text_channels:
                        if text_channel.topic == f"User ID - {ctx.message.author.id}":
                            ticketalreadymade = True
                    if ticketalreadymade == True:
                        alreadymade = discord.Embed(
                            title = "Ticket Error",
                            description = "You already have a ticket open!",
                            color = self.errorcolor
                        )
                        await ctx.send(embed = alreadymade)
                    else:
                        tickettopic = f"User ID - {ctx.message.author.id}"
                        ticketchannel = await ctx.guild.create_text_channel(ticketname, overwrites = overwrites, category = ticketcategory, topic = tickettopic)
                        creating = discord.Embed(
                            title = "Ticket",
                            description = "Creating your ticket!",
                            color = self.blurple
                        )
                        msg = await ctx.send(embed = creating)
                        await asyncio.sleep(3)
                        created = discord.Embed(
                            title = "Ticket",
                            description = f"Your ticket has been created {ticketchannel.mention}!",
                            color = self.blurple
                        )
                        if str(ctx.message.guild.id) not in mentions:
                            await ticketchannel.send("@here")
                        else:
                            mention  = mentions[str(ctx.message.guild.id)]
                            await ticketchannel.send(mention)
                        if reason == None:
                            ticketchannelmsg = discord.Embed(
                                title = "Ticket",
                                description = f"Hey {ctx.message.author.mention}, this is your ticket! Close this ticket with ``{prefix}close``.",
                                color = self.blurple
                            )
                        else:
                            ticketchannelmsg = discord.Embed(
                            title = "Ticket",
                            description = f"Hey {ctx.message.author.mention}, this is your ticket it was created with the reason {reason}! Close this ticket with ``{prefix}close``.",
                            color = self.blurple
                            )
                        await ticketchannel.send(embed = ticketchannelmsg)
                        await msg.edit(embed = created)
                        if str(ctx.message.guild.id) not in ticketlogchannels:
                            return
                        else:
                            ticketlogchannel = ticketlogchannels[str(ctx.message.guild.id)]
                            ticketlogchannel = discord.utils.get(ctx.guild.channels, id = ticketlogchannel)
                            if reason == None:
                                embed = discord.Embed(
                                    title = "Ticket",
                                    description = f"{ticketchannel.mention} `{ticketchannel}` has been created by {ctx.message.author.mention}",
                                    timestamp = datetime.datetime.utcnow(),
                                    color = self.blurple
                                )
                                await ticketlogchannel.send(embed = embed)
                            else:
                                embed = discord.Embed(
                                    title = "Ticket",
                                    description = f"{ticketchannel.mention} `{ticketchannel}` has been created by {ctx.message.author.mention} for {reason}",
                                    timestamp = datetime.datetime.utcnow(),
                                    color = self.blurple
                                )
                                await ticketlogchannel.send(embed = embed)
        except:
            embed = discord.Embed(
                title = "Ticket Error",
                description = "I could not perform this command, I do not have the correct permissions, make sure to give me all of [these](https://github.com/xPolar/WumpusMod/blob/master/README.md#required-permissions) permissions!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

    @ticket.error
    async def ticket_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
            title = "Cooldown",
            description = f"You can only make a ticket every 1m, try again in {int(error.retry_after)}s.",
            color = self.errorcolor
            )
            await ctx.send(embed = embed)
            await ctx.message.delete()

    @commands.command()
    async def close(self, ctx):
        """
        Close a ticket.
        """
        try:
            with open(r"PATHHERE\WumpusMod\Data\supportroles.json", "r") as f:
                supportroles = json.load(f)
            with open(r"PATHHERE\WumpusMod\Data\ticketcategorys.json", "r") as f:
                ticketcategorys = json.load(f)
            with open(r"PATHHERE\WumpusMod\Data\ticketlogchannels.json", "r") as f:
                ticketlogchannels = json.load(f)
            if str(ctx.message.guild.id) not in supportroles:
                embed = discord.Embed(
                    title = "Close Error",
                    description = "This server has no support role set!",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed)
            else:
                if str(ctx.message.guild.id) not in ticketcategorys:
                    embed = discord.Embed(
                        title = "Close Error",
                        description = "This server has no ticket category set!",
                        color = self.errorcolor
                    )
                    await ctx.send(embed = embed)
                else:
                    ticketcategory = ticketcategorys[str(ctx.message.guild.id)]
                    ticketcategory = discord.utils.get(ctx.guild.categories, id = ticketcategory)
                    if ctx.channel.category_id == ticketcategory.id:
                        supportrole  = supportroles[str(ctx.message.guild.id)]
                        supportrole = discord.utils.get(ctx.guild.roles, id = supportrole)
                        if ctx.channel.topic == f"User ID - {ctx.message.author.id}" or supportrole in ctx.message.author.roles:
                            await ctx.message.channel.delete()
                        else:
                            embed = discord.Embed(
                                title = "Close Error",
                                description = "You are not authorized to close this ticket!",
                                color = self.errorcolor
                            )
                            await ctx.send(embed = embed)
                        if str(ctx.message.guild.id) not in ticketlogchannels:
                            return
                        else:
                            ticketlogchannel = ticketlogchannels[str(ctx.message.guild.id)]
                            ticketlogchannel = discord.utils.get(ctx.guild.channels, id = ticketlogchannel)
                            embed = discord.Embed(
                                title = "Ticket",
                                description = f"`{ctx.message.channel.name}` has been closed by {ctx.message.author.mention}",
                                timestamp = datetime.datetime.utcnow(),
                                color = self.blurple
                            )
                            await ticketlogchannel.send(embed = embed)
                    else:
                        embed = discord.Embed(
                            title = "Close Error",
                            description = "This is not a ticket!",
                            color = self.errorcolor
                        )
                        await ctx.send(embed = embed)
        except:
            embed = discord.Embed(
                title = "Close Error",
                description = "I could not perform this command, I do not have the correct permissions, make sure to give me all of [these](https://github.com/xPolar/WumpusMod/blob/master/README.md#required-permissions) permissions!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

    @commands.command(aliases = ["useradd"])
    async def adduser(self, ctx, member : discord.Member = None):
        """
        Add a user to a ticket.
        """
        try:
            with open(r"PATHHERE\WumpusMod\Data\supportroles.json", "r") as f:
                supportroles = json.load(f)
            with open(r"PATHHERE\WumpusMod\Data\ticketcategorys.json", "r") as f:
                ticketcategorys = json.load(f)
            if str(ctx.message.guild.id) not in supportroles:
                embed = discord.Embed(
                    title = "Add Error",
                    description = "This server has no support role set!",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed)
            else:
                if str(ctx.message.guild.id) not in ticketcategorys:
                    embed = discord.Embed(
                        title = "Add Error",
                        description = "This server has no ticket category set!",
                        color = self.errorcolor
                    )
                    await ctx.send(embed = embed)
                else:
                    ticketcategory = ticketcategorys[str(ctx.message.guild.id)]
                    ticketcategory = discord.utils.get(ctx.guild.categories, id = ticketcategory)
                    if ctx.channel.category_id == ticketcategory.id:
                        supportrole  = supportroles[str(ctx.message.guild.id)]
                        supportrole = discord.utils.get(ctx.guild.roles, id = supportrole)
                        if supportrole in ctx.message.author.roles:
                            if member in ctx.message.channel.members:
                                embed = discord.Embed(
                                    title = "Add Error",
                                    description = "This user already has access to this ticket!",
                                    color = self.errorcolor
                                )
                                await ctx.send(embed = embed)
                            else:
                                await ctx.channel.set_permissions(member, read_messages = True, send_messages = True)
                                embed = discord.Embed(
                                    title = "Add",
                                    description = f"{member.mention} has been added to {ctx.message.channel.mention}",
                                    color = self.blurple
                                )
                                await ctx.send(member.mention, delete_after = 0.1)
                                await ctx.send(embed = embed)
                        else:
                            embed = discord.Embed(
                                title = "Add Error",
                                description = "You are not authorized to add users this ticket!",
                                color = self.errorcolor
                            )
                            await ctx.send(embed = embed)
        except:
            embed = discord.Embed(
                title = "Adduser Error",
                description = "I could not perform this command, I do not have the correct permissions, make sure to give me all of [these](https://github.com/xPolar/WumpusMod/blob/master/README.md#required-permissions) permissions!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

    @commands.command(aliases = ["userremove"])
    async def removeuser(self, ctx, member : discord.Member = None):
        """
        Remove a user from a ticket
        """
        try:
            with open(r"PATHHERE\WumpusMod\Data\supportroles.json", "r") as f:
                supportroles = json.load(f)
            with open(r"PATHHERE\WumpusMod\Data\ticketcategorys.json", "r") as f:
                ticketcategorys = json.load(f)
            if str(ctx.message.guild.id) not in supportroles:
                embed = discord.Embed(
                    title = "Remove Error",
                    description = "This server has no support role set!",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed)
            else:
                if str(ctx.message.guild.id) not in ticketcategorys:
                    embed = discord.Embed(
                        title = "Remove Error",
                        description = "This server has no ticket category set!",
                        color = self.errorcolor
                    )
                    await ctx.send(embed = embed)
                else:
                    ticketcategory = ticketcategorys[str(ctx.message.guild.id)]
                    ticketcategory = discord.utils.get(ctx.guild.categories, id = ticketcategory)
                    if ctx.channel.category_id == ticketcategory.id:
                        supportrole  = supportroles[str(ctx.message.guild.id)]
                        supportrole = discord.utils.get(ctx.guild.roles, id = supportrole)
                        if supportrole in ctx.message.author.roles:
                            if member not in ctx.message.channel.members:
                                embed = discord.Embed(
                                    title = "Remove Error",
                                    description = "This user never had access to this ticket!",
                                    color = self.errorcolor
                                )
                                await ctx.send(embed = embed)
                            else:
                                await ctx.channel.set_permissions(member, read_messages = False, send_messages = False)
                                embed = discord.Embed(
                                    title = "Remove",
                                    description = f"{member.mention} has been removed from {ctx.message.channel.mention}",
                                    color = self.blurple
                                )
                                await ctx.send(embed = embed)
                        else:
                            embed = discord.Embed(
                                title = "Remove Error",
                                description = "You are not authorized to remove users this ticket!",
                                color = self.errorcolor
                            )
                            await ctx.send(embed = embed)
        except:
            embed = discord.Embed(
                title = "Removeusers Error",
                description = "I could not perform this command, I do not have the correct permissions, make sure to give me all of [these](https://github.com/xPolar/WumpusMod/blob/master/README.md#required-permissions) permissions!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def supportrole(self, ctx, *, role : discord.Role = None):
        """
        Set the role which can respond to tickets.
        """
        with open(r"PATHHERE\WumpusMod\Data\supportroles.json", "r") as f:
            supportroles = json.load(f)
        if role == None:
            embed = discord.Embed(
                title = "Supportrole Error",
                description = "Please specify a role!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)
        else:
            supportroles[str(ctx.guild.id)] = role.id
            embed = discord.Embed(
                title = "Supportrole",
                description = f"{ctx.message.guild}'s support role is  now {role}",
                color = self.blurple
            )
            await ctx.send(embed = embed)

            with open(r"PATHHERE\WumpusMod\Data\supportroles.json", "w") as f:
                json.dump(supportroles, f, indent = 4)

    @supportrole.error
    async def supportrole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "You are missing the **Manage Server** permission!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def ticketcategory(self, ctx, *, category : discord.CategoryChannel = None):
        """
        Set the category which tickets get funneled into.
        """
        with open(r"PATHHERE\WumpusMod\Data\ticketcategorys.json", "r") as f:
            ticketcategorys = json.load(f)
        if category == None:
            embed = discord.Embed(
                title = "Ticketcategory Error",
                description = "Please specify a category!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)
        else:
            ticketcategorys[str(ctx.guild.id)] = category.id
            embed = discord.Embed(
                title = "Ticketcategory",
                description = f"{ctx.message.guild}'s ticket category is  now {category}",
                color = self.blurple
            )
            await ctx.send(embed = embed)

            with open(r"PATHHERE\WumpusMod\Data\ticketcategorys.json", "w") as f:
                json.dump(ticketcategorys, f, indent = 4)

    @ticketcategory.error
    async def ticketcategory_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "You are missing the **Manage Server** permission!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def mention(self, ctx, *, mention = None):
        """
        Set the message sent when a ticket is made.
        """
        with open(r"PATHHERE\WumpusMod\Data\mentions.json", "r") as f:
            mentions = json.load(f)
        if role == None:
            embed = discord.Embed(
                title = "Mention Error",
                description = "Please provide a mention!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)
        else:
            mentions[str(ctx.guild.id)] = str(mention)
            embed = discord.Embed(
                title = "Mention",
                description = f"{ctx.message.guild}'s mention is now {mention}",
                color = self.blurple
            )
            await ctx.send(embed = embed)

            with open(r"PATHHERE\WumpusMod\Data\mentions.json", "w") as f:
                json.dump(mentions, f, indent = 4)

    @mention.error
    async def mention_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "You are missing the **Manage Server** permission!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def ticketlogchannel(self, ctx, *, channel : discord.TextChannel = None):
        """
        Set the channel which tickets log into.
        """
        with open(r"PATHHERE\WumpusMod\Data\ticketlogchannels.json", "r") as f:
            ticketlogchannels = json.load(f)
        if channel == None:
            embed = discord.Embed(
                title = "Ticketlog Error",
                description = "Please specify a channel!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)
        else:
            ticketlogchannels[str(ctx.guild.id)] = channel.id
            embed = discord.Embed(
                title = "Mention",
                description = f"{ctx.message.guild}'s ticket log channel is now {channel.mention}",
                color = self.blurple
            )
            await ctx.send(embed = embed)

            with open(r"PATHHERE\WumpusMod\Data\ticketlogchannels.json", "w") as f:
                json.dump(ticketlogchannels, f, indent = 4)

    @ticketlogchannel.error
    async def ticketlogchannel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "You are missing the **Manage Server** permission!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(ticket_system(bot))
