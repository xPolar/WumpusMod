#Imports
import discord
from discord.ext import commands

class tickets(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.errorcolor = 0xFF2B2B
        self.blurple = 0x7289DA

    #On guild join set up ticket stuff
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        role = discord.utils.get(guild.roles, name = "Supporter")
        if role == None:
            role = await guild.create_role(name = "Muted")
        ticketcategory = discord.utils.get(guild.categories, name = "Tickets")
        if ticketcategory == None:
            category_overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages = False),
                self.bot.user: discord.PermissionOverwrite(read_messages = True),
                supporter: discord.PermissionOverwrite(read_messages = True)
            }
            ticketcategory = await guild.create_category(name = "Tickets", overwrites = category_overwrites)

    #Ticket
    @commands.command()
    async def ticket(self, ctx, *, reason = None):
        supporter = discord.utils.get(ctx.guild.roles, name = "Supporter")
        if supporter == None:
            supporter = await ctx.guild.create_role(name = "Supporter")
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages = False),
            ctx.author: discord.PermissionOverwrite(read_messages = True),
            self.bot.user: discord.PermissionOverwrite(read_messages = True),
            supporter: discord.PermissionOverwrite(read_messages = True),
        }
        ticketcategory = discord.utils.get(ctx.guild.categories, name = "Tickets")
        if ticketcategory == None:
            category_overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages = False),
                self.bot.user: discord.PermissionOverwrite(read_messages = True),
                supporter: discord.PermissionOverwrite(read_messages = True)
            }
            ticketcategory = await ctx.guild.create_category(name = "Tickets", overwrites = category_overwrites)
        ticketname = f"{ctx.message.author.id}"
        ticketalreadymade = discord.utils.get(ctx.guild.text_channels, name = ticketname)
        if ticketalreadymade != None:
            alreadymade = discord.Embed(
                title = "Ticket Error",
                description = "You already have a ticket open!",
                color = self.errorcolor
            )
            await ctx.send(embed = alreadymade)
        else:
            if reason == None:
                tickettitle = f"{ctx.message.author.name}#{ctx.author.discriminator} - No reason provided"
                if ctx.message.author.nick == None:
                    tickettitle = f"{ctx.message.author.name}#{ctx.author.discriminator} - No reason provided"
                else:
                    tickettitle = f"{ctx.message.author.nick}#{ctx.author.discriminator} - No reason provided"
            else:
                if ctx.message.author.nick == None:
                    tickettitle = f"{ctx.message.author.name}#{ctx.author.discriminator} - {reason}"
                else:
                    tickettitle = f"{ctx.message.author.nick}#{ctx.author.discriminator} - {reason}"
            creating = discord.Embed(
            title = "Ticket",
            description = "Creating your ticket!",
            color = self.blurple
            )
            msg = await ctx.send(embed = creating)
            ticketchannel = await ctx.guild.create_text_channel(ticketname, overwrites = overwrites, category = ticketcategory, topic = tickettitle)
            created = discord.Embed(
            title = "Ticket",
            description = "Your ticket has been created!",
            color = self.blurple
            )
            await msg.edit(embed = created)
            ticketchannelmsg = discord.Embed(
            title = "Ticket",
            description = f"Hey {ctx.author.mention}, this is your ticket! Close this ticket with ``?close``, add users with ``?adduser (User)``, and ``?rmuser (User)``.",
            color = self.blurple
            )
            await ticketchannel.send(embed = ticketchannelmsg)
            await ticketchannel.send("@here", delete_after = 0.1)

    #Close
    @commands.command()
    async def close(self, ctx):
        supporter = discord.utils.get(ctx.guild.roles, name = "Supporter")
        if supporter == None:
            supporter = await ctx.guild.create_role(name = "Supporter")
        ticketcategory = discord.utils.get(ctx.guild.categories, name = "Tickets")
        if ctx.channel.category_id == ticketcategory.id:
            if ctx.channel.name == f"{ctx.message.author.id}" or supporter in ctx.message.author.roles:
                await ctx.channel.delete()
            else:
                notyourticket = discord.Embed(
                 title = "Close Error",
                 description = "You do not have permission to close this ticket!",
                 color = self.errorcolor
                )
                await ctx.send(embed = notyourticket)
        else:
            notinticket = discord.Embed(
                title = "Close Error",
                description = "This command needs to be used in a ticket!",
                color = self.errorcolor
            )
            await ctx.send(embed = notinticket)

    #Add user
    @commands.command()
    async def adduser(self, ctx, *, member : discord.Member = None):
        if member != None:
            supporter = discord.utils.get(ctx.guild.roles, name = "Supporter")
            if supporter == None:
                supporter = await ctx.guild.create_role(name = "Supporter")
            ticketcategory = discord.utils.get(ctx.guild.categories, name = "Tickets")
            if ctx.channel.category_id == ticketcategory.id:
                if ctx.channel.name == f"{ctx.message.author.id}" or supporter in ctx.message.author.roles:
                    if member in ctx.channel.members:
                        alreadyin = discord.Embed(
                            title = "Add Error",
                            description = "This user already has access to this channel.",
                            color = self.errorcolor
                        )
                        await ctx.send(embed = alreadyin)
                    else:
                        await ctx.channel.set_permissions(member, read_messages = True, send_messages = True)
                        successadd = discord.Embed(
                            title="Add",
                            description = f"I have added {member.mention} to this Ticket!",
                            color = self.blurple
                        )
                        mentionadded = await ctx.send(member.mention)
                        await mentionadded.delete()
                        await ctx.send(embed = successadd)
                else:
                    notyourticket = discord.Embed(
                    title="Add Error",
                    description="You do not have permission to close this ticket!",
                    color = self.errorcolor
                    )
                    await ctx.send(embed = notyourticket)
            else:
                notinticket = discord.Embed(
                    title="Add Error",
                    description="This command must be used in a Ticket Channel!",
                    color = self.errorcolor
                )
                await ctx.send(embed = notinticket)
        else:
            specify = discord.Embed(
                title="Ticket Error",
                description="Please Specify a User!",
                color = self.errorcolor
            )
            await ctx.send(embed=specify)
            return

    #Remove user
    @commands.command(aliases = ["rmuser"])
    async def removeuser(self, ctx, *, member : discord.Member = None):
        if member != None:
            supporter = discord.utils.get(ctx.guild.roles, name = "Supporter")
            if supporter == None:
                supporter = await ctx.guild.create_role(name = "Supporter")
            ticketcategory = discord.utils.get(ctx.guild.categories, name="Tickets")
            if ctx.channel.category_id == ticketcategory.id:
                if ctx.channel.name == f"{ctx.message.author.id}" or supporter in ctx.message.author.roles:
                    if member not in ctx.channel.members:
                        alreadyin = discord.Embed(
                            title = "Remove Error",
                            description = "This user does not have access to this ticket.",
                            color = self.errorcolor
                        )
                        await ctx.send(embed = alreadyin)
                    if supporter in member.roles:
                        embed = discord.Embed(
                            title = "Remove Error",
                            description = "You can't remove a support member from a ticket!",
                            color = self.errorcolor
                        )
                    else:
                        await ctx.channel.set_permissions(member, read_messages = False, send_messages = False)
                        successadd = discord.Embed(
                            title = "Remove",
                            description = f"I have removed {member.mention} from this Ticket!",
                            color = self.blurple
                        )
                        mentionadded = await ctx.send(member.mention)
                        await mentionadded.delete()
                        await ctx.send(embed=successadd)
                else:
                    notyourticket = discord.Embed(
                        title = "Remove Error",
                        description = "This is not your Ticket!",
                        color = self.errorcolor
                    )
                    await ctx.send(embed=notyourticket)
            else:
                notinticket = discord.Embed(
                    title = "Remove Error",
                    description = "This command must be used in a Ticket Channel!",
                    color = self.errorcolor
                )
                await ctx.send(embed=notinticket)
        else:
            specify = discord.Embed(
                title = "Remove Error",
                description = "Please Specify a User!",
                color = self.errorcolor
            )
            await ctx.send(embed=specify)
            return

    #Supporteradd command
    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def supporteradd(self, ctx, member : discord.Member = None):
        if member == None:
            embed = discord.Embed(
                title = "Supporteradd Error",
                description = "Please specify a user!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)
        else:
            role = discord.utils.get(ctx.guild.roles, name = "Supporter")
            await member.add_roles(role)
            added = discord.Embed(
                title = "Supportadd",
                description = f"I have made {member.mention} a supporter!",
                color = self.blurple
            )
            await ctx.send(embed = added)

def setup(bot):
    bot.add_cog(tickets(bot))
