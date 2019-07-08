import discord
from discord.ext import commands

class moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.errorcolor = 0xFF2B2B
        self.blurple = 0x7289DA
        self.required_permissions = discord.Embed(
            title = "Missing Permissions",
            description = "I am missing some permissions, make sure to give me access to all of [these](https://github.com/xPolar/WumpusMod#required-permissions) permissions!",
            color = 0xFF2B2B
        )

    #On guild join set up mute stuff
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        role = discord.utils.get(guild.roles, name = "Muted")
        if role == None:
            role = await guild.create_role(name = "Muted")
        for channel in guild.text_channels:
            await channel.set_permissions(role, send_messages = False)

    #On channel create set up mute stuff
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild = channel.guild
        role = discord.utils.get(guild.roles, name = "Muted")
        if role == None:
            role = await guild.create_role(name = "Muted")
        await channel.set_permissions(role, send_messages = False)

    #Purge command
    @commands.command(aliases = ["clear"])
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, amount = 10):
        try:
            max_purge = 500
            if amount >= 1 and amount <= max_purge:
                await ctx.channel.purge(limit = amount + 1)
                embed = discord.Embed(
                    title = "Purge",
                    description = f"Purged {amount} message(s)!",
                    color = self.blurple
                )
                await ctx.send(embed = embed, delete_after = 5.0)
                modlog = discord.utils.get(ctx.guild.text_channels, name = "modlog")
                if modlog == None:
                    return
                if modlog != None:
                    embed = discord.Embed(
                        title = "Purge",
                        description = f"{amount} message(s) have been purged by {ctx.author.mention} in {ctx.message.channel.mention}",
                        color = self.blurple
                    )
                    await modlog.send(embed = embed)
            if amount < 1:
                embed = discord.Embed(
                    title = "Purge Error",
                    description = f"You must purge more then {amount} message(s)!",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed, delete_after = 5.0)
                await ctx.message.delete()
            if amount > max_purge:
                embed = discord.Embed(
                    title = "Purge Error",
                    description = f"You must purge less then {amount} messages!",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed, delete_after = 5.0)
                await ctx.message.delete()
        except:
            await ctx.send(embed = self.required_permissions)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "You are missing the **Manage Messages(s)** permission!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)
            await ctx.message.delete()

    #Kick command
    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member : discord.Member = None, *, reason = None):
        try:
            if member == None:
                embed = discord.Embed(
                    title = "Kick Error",
                    description = "Please specify a member!",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed, delete_after = 5.0)
            else:
                    if reason == None:
                        await member.kick(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - No reason proivded.")
                        embed = discord.Embed(
                            title = "Kick",
                            description = f"{member.mention} has been kicked by {ctx.message.author.mention}.",
                            color = self.blurple
                        )
                        await ctx.send(embed = embed)
                        modlog = discord.utils.get(ctx.guild.text_channels, name = "modlog")
                        if modlog == None:
                            return
                        if modlog != None:
                            embed = discord.Embed(
                                title = "Kick",
                                description = f"{member.mention} has been kicked by {ctx.message.author.mention} in {ctx.message.channel.mention}.",
                                color = self.blurple
                            )
                            await modlog.send(embed = embed)
                    else:
                        await member.kick(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - {reason}")
                        embed = discord.Embed(
                            title = "Kick",
                            description = f"{member.mention} has been kicked by {ctx.message.author.mention} for {reason}",
                            color = self.blurple
                        )
                        await ctx.send(embed = embed)
                        modlog = discord.utils.get(ctx.guild.text_channels, name = "modlog")
                        if modlog == None:
                            return
                        if modlog != None:
                            embed = discord.Embed(
                                title = "Kick",
                                description = f"{member.mention} has been kicked by {ctx.message.author.mention} in {ctx.message.channel.mention} for {reason}",
                                color = self.blurple
                            )
                            await modlog.send(embed = embed)
        except:
            await ctx.send(embed = self.required_permissions)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "You are missing the **Kick Member(s)** permission!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)

    #Ban command
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member = None, *, reason = None):
        try:
            if member == None:
                embed = discord.Embed(
                    title = "Ban Error",
                    description = "Please specify a user!",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed)
            else:
                if reason == None:
                    await member.ban(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - No Reason Provided.")
                    embed = discord.Embed(
                        title = "Ban",
                        description = f"{member.mention} has been banned by {ctx.message.author.mention}.",
                        color = self.blurple
                    )
                    modlog = discord.utils.get(ctx.guild.text_channels, name = "modlog")
                    if modlog == None:
                        return
                    if modlog != None:
                        embed = discord.Embed(
                            title = "Ban",
                            description = f"{member.mention} has been banned by {ctx.message.author.mention}.",
                            color = self.blurple
                        )
                        await modlog.send(embed = embed)
                else:
                    await member.ban(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}.\nReason - {reason}")
                    embed = discord.Embed(
                        title = "Ban",
                        description = f"{member.mention} has been banend by {ctx.message.author.mention} for {reason}",
                        color = self.blurple
                    )
                    await ctx.send(embed = embed)
                    modlog = discord.utils.get(ctx.guild.text_channels, name = "modlog")
                    if modlog == None:
                        return
                    if modlog != None:
                        embed = discord.Embed(
                            title = "Ban",
                            description = f"{member.mention} has been banned by {ctx.message.author.mention} in {ctx.message.channel.mention} for {reason}",
                            color = self.blurple
                        )
                        await modlog.send(embed = embed)
        except:
            await ctx.send(embed = self.required_permissions)


    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "You are missing the **Ban Member(s)** permission!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)

    #Unban command
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, *, member : discord.User = None):
        try:
            if member == None:
                embed = discord.Embed(
                    title = "Unban Error",
                    description = "Please specify a user!",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed, delete_after = 5.0)
            else:
                banned_users = await ctx.guild.bans()
                for ban_entry in banned_users:
                    user = ban_entry.user

                    if (user.name, user.discriminator) == (member.name, member.discriminator):
                        embed = discord.Embed(
                            title = "Unban",
                            description = f"Unbanned {user.mention}",
                            color = self.blurple
                        )
                        await ctx.guild.unban(user)
                        await ctx.send(embed = embed)
                        modlog = discord.utils.get(ctx.guild.text_channels, name = "modlog")
                        if modlog == None:
                            return
                        if modlog != None:
                            embed = discord.Embed(
                                title = "Ban",
                                description = f"{user.mention} has been unbanned by {ctx.message.author.mention} in {ctx.message.channel.mention}.",
                                color = self.blurple
                            )
                            await modlog.send(embed = embed)
        except:
            await ctx.send(embed = self.required_permissions)


    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "You are missing the **Ban Member(s)** permission!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed, delete_after = 5.0)

    #Mute command
    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def mute(self, ctx, member : discord.Member = None, *, reason = None):
        try:
            if member == None:
                embed = discord.Embed(
                    title = "Mute Error",
                    description = "Please specify a user!",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed, delete_after = 5.0)
            else:
                if member.id == ctx.message.author.id:
                    embed = discord.Embed(
                        title = "Mute Error",
                        description = "You can't mute yourself!",
                        color = self.errorcolor
                    )
                    await ctx.send(embed = embed, delete_after = 5.0)
                else:
                    if reason == None:
                        role = discord.utils.get(ctx.guild.roles, name = "Muted")
                        if role == None:
                            role = await ctx.guild.create_role(name = "Muted")
                            for channel in ctx.guild.text_channels:
                                await channel.set_permissions(role, send_messages = False)
                        await member.add_roles(role)
                        embed = discord.Embed(
                            title = "Mute",
                            description = f"{member.mention} has been muted by {ctx.message.author.mention}.",
                            color = self.blurple
                        )
                        await ctx.send(embed = embed)
                        modlog = discord.utils.get(ctx.guild.text_channels, name = "modlog")
                        if modlog == None:
                            return
                        if modlog != None:
                            embed = discord.Embed(
                                title = "Mute",
                                description = f"{member.mention} has been muted by {ctx.message.author.mention} in {ctx.message.channel.mention}.",
                                color = self.blurple
                            )
                            await modlog.send(embed = embed)
                    else:
                        role = discord.utils.get(ctx.guild.roles, name = "Muted")
                        if role == None:
                            role = await ctx.guild.create_role(name = "Muted")
                            for channel in ctx.guild.text_channels:
                                await channel.set_permissions(role, send_messages = False)
                        await member.add_roles(role)
                        embed = discord.Embed(
                            title = "Mute",
                            description = f"{member.mention} has been muted by {ctx.message.author.mention} for {reason}",
                            color = self.blurple
                        )
                        await ctx.send(embed = embed)
                        modlog = discord.utils.get(ctx.guild.text_channels, name = "modlog")
                        if modlog == None:
                            return
                        if modlog != None:
                            embed = discord.Embed(
                                title = "Mute",
                                description = f"{member.mention} has been muted by {ctx.message.author.mention} in {ctx.message.channel.mention} for {reason}",
                                color = self.blurple
                            )
                            await modlog.send(embed = embed)
        except:
            await ctx.send(embed = self.required_permissions)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions!",
                description = "You are missing the **Manage Role(s)** permission!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

    #Unmute command
    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def unmute(self, ctx, member : discord.Member = None):
        try:
            if member == None:
                embed = discord.Embed(
                    title = "Unmute Error",
                    description = "Please specify a user!",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed, delete_after = 5.0)
            else:
                role = discord.utils.get(ctx.guild.roles, name = "Muted")
                if role in member.roles:
                    await member.remove_roles(role)
                    embed = discord.Embed(
                        title = "Unmute",
                        description = f"{member.mention} has been unmuted by {ctx.message.author.mention}.",
                        color = self.blurple
                    )
                    await ctx.send(embed = embed)
                    modlog = discord.utils.get(ctx.guild.text_channels, name = "modlog")
                    if modlog == None:
                        return
                    if modlog != None:
                        embed = discord.Embed(
                            title = "Unmute",
                            description = f"{member.mention} has been unmuted by {ctx.message.author.mention} in {ctx.message.channel.mention}.",
                            color = self.blurple
                        )
                        await modlog.send(embed = embed)
                else:
                    embed = discord.Embed(
                        title = "Unmute Error",
                        description = f"{member.mention} is not muted!",
                        color = self.errorcolor
                    )
                    await ctx.send(embed = embed)
        except:
            await ctx.send(embed = self.required_permissions)

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions!",
                description = "You are missing the **Manage Role(s)** permission!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(moderation(bot))
