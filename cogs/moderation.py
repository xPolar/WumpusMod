import asyncio
import datetime
import discord
from discord.ext import commands
import json

class moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.errorcolor = 0xFF2B2B
        self.blurple = 0x7289DA

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        role = discord.utils.get(guild.roles, name = "Muted")
        if role == None:
            return
        else:
            for channel in guild.text_channels:
                await channel.set_permissions(role, send_messages = False)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild = channel.guild
        role = discord.utils.get(guild.roles, name = "Muted")
        if role == None:
            return
        else:
            await channel.set_permissions(role, send_messages = False)

    @commands.command(aliases = ["clear"])
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, amount = None):
        """
        Delete a large amount of messages, up to 1000.
        """
        try:
            if amount == None:
                amount = 10
            else:
                with open(r"PATHHERE\WumpusMod\Data\modlogs.json", "r") as f:
                    modlogs = json.load(f)
                max_purge = 1000
                if amount >= 1 and amount <= max_purge:
                    message = ctx.message
                    await ctx.channel.purge(limit = amount + 1)
                    embed = discord.Embed(
                        title = "Purge",
                        description = f"Purged {amount} message(s)!",
                        color = self.blurple
                    )
                    await ctx.send(embed = embed, delete_after = 5.0)
                    if str(ctx.message.guild.id) in modlogs:
                        modlog = modlogs[str(ctx.message.guild.id)]
                        modlog = discord.utils.get(ctx.guild.channels, id = modlog)
                        embed = discord.Embed(
                            title = "Purge",
                            description = f"{message.author.mention} has purged {amount} message(s) in {message.channel.mention}.",
                            timestamp = datetime.datetime.utcnow(),
                            color = self.blurple
                        )
                        await modlog.send(embed = embed)
                if amount < 1:
                    embed = discord.Embed(
                        title = "Purge Error",
                        description = "You must purge more then 0 message!",
                        color = self.errorcolor
                    )
                    await ctx.send(embed = embed)
                if amount > max_purge:
                    embed = discord.Embed(
                        title = "Purge Error",
                        description = "You must purge 1000 or less messages!",
                        color = self.errorcolor
                    )
                    await ctx.send(embed = embed)
        except:
            embed = discord.Embed(
                title = "Purge Error",
                description = "I could not perform this command, I do not have the correct permissions, make sure to give me all of [these](https://github.com/xPolar/WumpusMod/blob/master/README.md#required-permissions) permissions!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "You are missing the **Manage Message(s)** permission!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member : discord.Member = None, *, reason = None):
        """
        Kick a user from the server.
        """
        try:
            with open(r"PATHHERE\WumpusMod\Data\modlogs.json", "r") as f:
                modlogs = json.load(f)
            if member == None:
                embed = discord.Embed(
                    title = "Kick Error",
                    description = "Please specify a member!",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed)
            else:
                if member.id == ctx.message.author.id:
                    embed = discord.Embed(
                        title = "Kick Error",
                        description = "You can not kick yourself!",
                        color = self.errorcolor
                    )
                    await ctx.send(embed = embed)
                else:
                    if reason == None:
                        await member.kick(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}")
                        embed = discord.Embed(
                            title = "Kick",
                            description = f"{member.mention} has been kicked by {ctx.message.author.mention}",
                            color = self.blurple
                        )
                        await ctx.send(embed = embed)
                        if str(ctx.message.guild.id) in modlogs:
                            modlog = modlogs[str(ctx.message.guild.id)]
                            modlog = discord.utils.get(ctx.guild.channels, id = modlog)
                            embed = discord.Embed(
                                title = "Kick",
                                description = f"{ctx.message.author.mention} has kicked {member.mention} in {ctx.message.channel.mention}",
                                timestamp = datetime.datetime.utcnow(),
                                color = self.blurple
                            )
                            await modlog.send(embed = embed)
                    else:
                        await member.kick(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}\nReason - {reason}")
                        embed = discord.Embed(
                            title = "Kick",
                            description = f"{member.mention} has been kicked by {ctx.message.author.mention} for {reason}",
                            color = self.blurple
                        )
                        await ctx.send(embed = embed)
                        if str(ctx.message.guild.id) in modlogs:
                            modlog = modlogs[str(ctx.message.guild.id)]
                            modlog = discord.utils.get(ctx.guild.channels, id = modlog)
                            embed = discord.Embed(
                                title = "Kick",
                                description = f"{ctx.message.author.mention} has kicked {member.mention} in {ctx.message.channel.mention} for {reason}",
                                timestamp = datetime.datetime.utcnow(),
                                color = self.blurple
                            )
                            await modlog.send(embed = embed)
        except:
            embed = discord.Embed(
                title = "Kick Error",
                description = "I could not perform this command, one of two things may have happend!\n- I do not have the correct permissions, make sure to give me all of [these](https://github.com/xPolar/WumpusMod/blob/master/README.md#required-permissions) permissions!\n- Role hiearchy has prevented me from doing this.",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title = "Missing Permissions",
                description = "You are missing the **Kick Member(s)** permission!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member = None, *, reason = None):
        """
        Ban a user from the server.
        """
        try:
            with open(r"PATHHERE\WumpusMod\Data\modlogs.json", "r") as f:
                modlogs = json.load(f)
            if member == None:
                embed = discord.Embed(
                    title = "Ban Error",
                    description = "Please specify a member!",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed)
            else:
                if member.id == ctx.message.author.id:
                    embed = discord.Embed(
                        title = "Ban Error",
                        description = "You can not ban yourself!",
                        color = self.errorcolor
                    )
                    await ctx.send(embed = embed)
                else:
                    if reason == None:
                        await member.ban(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}")
                        embed = discord.Embed(
                            title = "Ban",
                            description = f"{member.mention} has been banned by {ctx.message.author.mention}",
                            color = self.blurple
                        )
                        await ctx.send(embed = embed)
                        if str(ctx.message.guild.id) in modlogs:
                            modlog = modlogs[str(ctx.message.guild.id)]
                            modlog = discord.utils.get(ctx.guild.channels, id = modlog)
                            embed = discord.Embed(
                                title = "Ban",
                                description = f"{ctx.message.author.mention} has banned {member.mention} in {ctx.message.channel.mention}",
                                timestamp = datetime.datetime.utcnow(),
                                color = self.blurple
                            )
                            await modlog.send(embed = embed)
                    else:
                        await member.ban(reason = f"Moderator - {ctx.message.author.name}#{ctx.message.author.discriminator}\nReason - {reason}")
                        embed = discord.Embed(
                            title = "Ban",
                            description = f"{member.mention} has been banned by {ctx.message.author.mention} for {reason}",
                            color = self.blurple
                        )
                        await ctx.send(embed = embed)
                        if str(ctx.message.guild.id) in modlogs:
                            modlog = modlogs[str(ctx.message.guild.id)]
                            modlog = discord.utils.get(ctx.guild.channels, id = modlog)
                            embed = discord.Embed(
                                title = "Ban",
                                description = f"{ctx.message.author.mention} has banned {member.mention} in {ctx.message.channel.mention} for {reason}",
                                timestamp = datetime.datetime.utcnow(),
                                color = self.blurple
                            )
                            await modlog.send(embed = embed)
        except:
            embed = discord.Embed(
                title = "Ban Error",
                description = "I could not perform this command, one of two things may have happend!\n- I do not have the correct permissions, make sure to give me all of [these](https://github.com/xPolar/WumpusMod/blob/master/README.md#required-permissions) permissions!\n- Role hiearchy has prevented me from doing this.",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, *, member : discord.User = None):
        """
        Unban a user from the server.
        """
        try:
            with open(r"PATHHERE\WumpusMod\Data\modlogs.json", "r") as f:
                modlogs = json.load(f)
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
                        if str(ctx.message.guild.id) in modlogs:
                            modlog = modlogs[str(ctx.message.guild.id)]
                            modlog = discord.utils.get(ctx.guild.text_channels, id = modlog)
                            embed = discord.Embed(
                                title = "Unban",
                                description = f"{user.mention} has been unbanned by {ctx.message.author.mention} in {ctx.message.channel.mention}.",
                                timestamp = datetime.datetime.utcnow(),
                                color = self.blurple
                            )
                            await modlog.send(embed = embed)
        except:
            embed = discord.Embed(
                title = "Unban Error",
                description = "I could not perform this command, I do not have the correct permissions, make sure to give me all of [these](https://github.com/xPolar/WumpusMod/blob/master/README.md#required-permissions) permissions!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def mute(self, ctx, member : discord.Member = None, time = None, *, reason = None):
        """
        Mutes a user so they can't talk.
        """
        try:
            with open(r"PATHHERE\WumpusMod\Data\modlogs.json", "r") as f:
                modlogs = json.load(f)
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
                    with open(r"PATHHERE\WumpusMod\Data\muteroles.json", "r") as f:
                        muteroles = json.load(f)
                    if str(ctx.message.guild.id) in muteroles:
                        muterole = muteroles[str(ctx.message.guild.id)]
                        muterole = discord.utils.get(ctx.message.guild.roles, id = muterole)
                        if reason == None:
                            if time == None:
                                await member.add_roles(muterole)
                                embed = discord.Embed(
                                    title = "Mute",
                                    description = f"{member.mention} has been muted by {ctx.message.author.mention}",
                                    color = self.blurple
                                )
                                await ctx.send(embed = embed)
                                if str(ctx.message.guild.id) in modlogs:
                                    modlog = modlogs[str(ctx.message.guild.id)]
                                    modlog = discord.utils.get(ctx.guild.text_channels, id = modlog)
                                    embed = discord.Embed(
                                        title = "Muted",
                                        description = f"{member.mention} has been muted by {ctx.message.author.mention} in {ctx.message.channel.mention}.",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.blurple
                                    )
                                    await modlog.send(embed = embed)
                            else:
                                await member.add_roles(muterole)
                                if time.endswith(("s", "m", "h", "d", "w", "y")) != True:
                                    embed = discord.Embed(
                                        title = "Mute Error",
                                        description = "Please provide a correct time",
                                        color = self.errorcolor
                                    )
                                    await ctx.send(embed = embed)
                                else:
                                    if time.endswith("s") == True:
                                        time_1 = time.replace("s", "")
                                        unmute_after = int(time_1)
                                    if time.endswith("m") == True:
                                        time_1 = time.replace("m", "")
                                        unmute_after = int(time_1) * 60
                                    if time.endswith("h") == True:
                                        time_1 = time.replace("h", "")
                                        unmute_after = int(time_1) * 3600
                                    if time.endswith("d") == True:
                                        time_1 = time.replace("d", "")
                                        unmute_after = int(time_1) * 86400
                                    if time.endswith("w") == True:
                                        time_1 = time.replace("w", "")
                                        unmute_after = int(time_1) * 604800
                                    if time.endswith("y") == True:
                                        time_1 = time.replace("y", "")
                                        unmute_after = int(time_1) * 31536000
                                    await member.add_roles(muterole)
                                    embed = discord.Embed(
                                        title = "Mute",
                                        description = f"{member.mention} has been muted by {ctx.message.author.mention} for {time}",
                                        color = self.blurple
                                    )
                                    await ctx.send(embed = embed)
                                    if str(ctx.message.guild.id) in modlogs:
                                        modlog = modlogs[str(ctx.message.guild.id)]
                                        modlog = discord.utils.get(ctx.guild.text_channels, id = modlog)
                                        embed = discord.Embed(
                                            title = "Mute",
                                            description = f"{member.mention} has been muted by {ctx.message.author.mention} in {ctx.message.channel.mention} for {time}.",
                                            timestamp = datetime.datetime.utcnow(),
                                            color = self.blurple
                                        )
                                        await modlog.send(embed = embed)
                                    await asyncio.sleep(unmute_after)
                                    await member.remove_roles(muterole)
                        else:
                            if time == None:
                                await member.add_roles(muterole)
                                embed = discord.Embed(
                                    title = "Mute",
                                    description = f"{member.mention} has been muted by {ctx.message.author.mention} for {reason}",
                                    color = self.blurple
                                )
                                await ctx.send(embed = embed)
                                if str(ctx.message.guild.id) in modlogs:
                                    modlog = modlogs[str(ctx.message.guild.id)]
                                    modlog = discord.utils.get(ctx.guild.text_channels, id = modlog)
                                    embed = discord.Embed(
                                        title = "Muted",
                                        description = f"{member.mention} has been muted by {ctx.message.author.mention} in {ctx.message.channel.mention} for {reason}.",
                                        timestamp = datetime.datetime.utcnow(),
                                        color = self.blurple
                                    )
                                    await modlog.send(embed = embed)
                            else:
                                await member.add_roles(muterole)
                                if time.endswith(("s", "m", "h", "d", "w", "y")) != True:
                                    embed = discord.Embed(
                                        title = "Mute Error",
                                        description = "Please provide a correct time",
                                        color = self.errorcolor
                                    )
                                    await ctx.send(embed = embed)
                                else:
                                    if time.endswith("s") == True:
                                        time_1 = time.replace("s", "")
                                        unmute_after = int(time_1)
                                    if time.endswith("m") == True:
                                        time_1 = time.replace("m", "")
                                        unmute_after = int(time_1) * 60
                                    if time.endswith("h") == True:
                                        time_1 = time.replace("h", "")
                                        unmute_after = int(time_1) * 3600
                                    if time.endswith("d") == True:
                                        time_1 = time.replace("d", "")
                                        unmute_after = int(time_1) * 86400
                                    if time.endswith("w") == True:
                                        time_1 = time.replace("w", "")
                                        unmute_after = int(time_1) * 604800
                                    if time.endswith("y") == True:
                                        time_1 = time.replace("y", "")
                                        unmute_after = int(time_1) * 31536000
                                    await member.add_roles(muterole)
                                    embed = discord.Embed(
                                        title = "Mute",
                                        description = f"{member.mention} has been muted by {ctx.message.author.mention} for {reason} for {time}",
                                        color = self.blurple
                                    )
                                    await ctx.send(embed = embed)
                                    if str(ctx.message.guild.id) in modlogs:
                                        modlog = modlogs[str(ctx.message.guild.id)]
                                        modlog = discord.utils.get(ctx.guild.text_channels, id = modlog)
                                        embed = discord.Embed(
                                            title = "Mute",
                                            description = f"{member.mention} has been muted by {ctx.message.author.mention} in {ctx.message.channel.mention} for {reason} for {time}.",
                                            timestamp = datetime.datetime.utcnow(),
                                            color = self.blurple
                                        )
                                        await modlog.send(embed = embed)
                                    await asyncio.sleep(unmute_after)
                                    await member.remove_roles(muterole)
                    else:
                        embed = discord.Embed(
                            title = "Mute Error",
                            description = "This server has no mute role set!",
                            color = self.errorcolor
                        )
                        await ctx.send(embed = embed)
        except:
            embed = discord.Embed(
                title = "Mute Error",
                description = "I could not perform this command, one of two things may have happend!\n- I do not have the correct permissions, make sure to give me all of [these](https://github.com/xPolar/WumpusMod/blob/master/README.md#required-permissions) permissions!\n- Role hiearchy has prevented me from doing this.",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def unmute(self, ctx, member : discord.Member = None, *, reason = None):
        """
        Unmutes a user so they can talk.
        """
        try:
            with open(r"PATHHERE\WumpusMod\Data\modlogs.json", "r") as f:
                modlogs = json.load(f)
            if member == None:
                embed = discord.Embed(
                    title = "Unmute Error",
                    description = "Please specify a user!",
                    color = self.errorcolor
                )
                await ctx.send(embed = embed)
            else:
                with open(r"PATHHERE\WumpusMod\Data\muteroles.json", "r") as f:
                    muteroles = json.load(f)
                if str(ctx.message.guild.id) in muteroles:
                    muterole = muteroles[str(ctx.message.guild.id)]
                    muterole = discord.utils.get(ctx.message.guild.roles, id = muterole)
                    check_for_muterole_on_user = discord.utils.get(ctx.message.author.roles, id = muterole)
                    if check_for_muterole_on_user == None:
                        embed = discord.Embed(
                            title = "Unmute Error",
                            description = "This user is not muted!",
                            color = self.errorcolor
                        )
                        await ctx.send(embed = embed)
                    else:
                        if reason == None:
                            await member.remove_roles(muterole)
                            embed = discord.Embed(
                                title = "Unmute",
                                description = f"{member.mention} has been unmuted by {ctx.message.author.mention}",
                                color = self.blurple
                            )
                            await ctx.send(embed = embed)
                            if str(ctx.message.guild.id) in modlogs:
                                modlog = modlogs[str(ctx.message.guild.id)]
                                modlog = discord.utils.get(ctx.guild.text_channels, id = modlog)
                                embed = discord.Embed(
                                    title = "Unmuted",
                                    description = f"{member.mention} has been unmuted by {ctx.message.author.mention} in {ctx.message.channel.mention}.",
                                    timestamp = datetime.datetime.utcnow(),
                                    color = self.blurple
                                )
                                await modlog.send(embed = embed)
                        else:
                            await member.remove_roles(muterole)
                            embed = discord.Embed(
                                title = "Unmute",
                                description = f"{member.mention} has been unmuted by {ctx.message.author.mention} for {reason}",
                                color = self.blurple
                            )
                            await ctx.send(embed = embed)
                            if str(ctx.message.guild.id) in modlogs:
                                modlog = modlogs[str(ctx.message.guild.id)]
                                modlog = discord.utils.get(ctx.guild.text_channels, id = modlog)
                                embed = discord.Embed(
                                    title = "Unmuted",
                                    description = f"{member.mention} has been unmuted by {ctx.message.author.mention} in {ctx.message.channel.mention} for {reason}.",
                                    timestamp = datetime.datetime.utcnow(),
                                    color = self.blurple
                                )
                                await modlog.send(embed = embed)
        except:
            embed = discord.Embed(
                title = "Unmute Error",
                description = "I could not perform this command, one of two things may have happend!\n- I do not have the correct permissions, make sure to give me all of [these](https://github.com/xPolar/WumpusMod/blob/master/README.md#required-permissions) permissions!\n- Role hiearchy has prevented me from doing this.",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def nuke(self, ctx, *, reason = None):
        """
        Delete all the messages in a channel.
        """
        try:
            with open(r"PATHHERE\WumpusMod\Data\modlogs.json", "r") as f:
                modlogs = json.load(f)
            if reason == None:
                position = ctx.message.channel.position
                channel = await ctx.message.channel.clone(reason = f"Nuke done by {ctx.message.author.name}#{ctx.message.author.discriminator}")
                await channel.edit(position = position)
                await ctx.message.channel.delete(reason = f"Nuke done by {ctx.message.author.name}#{ctx.message.author.discriminator}")
                embed = discord.Embed(
                    title = "Nuke",
                    description = f"Nuke done by {ctx.message.author.mention}",
                    color = self.blurple
                )
                embed.set_image(url = "https://imgur.com/LIyGeCR.gif")
                await channel.send(embed = embed, delete_after = 120)
                if str(ctx.message.guild.id) in modlogs:
                    modlog = modlogs[str(ctx.message.guild.id)]
                    modlog = discord.utils.get(ctx.guild.text_channels, id = modlog)
                    embed = discord.Embed(
                        title = "Nuke",
                        description = f"{channel.mention} has been nuked by {ctx.message.author.mention}.",
                        timestamp = datetime.datetime.utcnow(),
                        color = self.blurple
                    )
                    await modlog.send(embed = embed)
            else:
                position = ctx.message.channel.position
                channel = await ctx.message.channel.clone(reason = f"Nuke done by {ctx.message.author.name}#{ctx.message.author.discriminator} for {reason}")
                await channel.edit(position = position)
                await ctx.message.channel.delete(reason = f"Nuke done by {ctx.message.author.name}#{ctx.message.author.discriminator} for {reason}")
                embed = discord.Embed(
                    title = "Nuke",
                    description = f"Nuke done by {ctx.message.author.mention} for {reason}",
                    color = self.blurple
                )
                embed.set_image(url = "https://imgur.com/LIyGeCR.gif")
                await channel.send(embed = embed, delete_after = 120)
                if str(ctx.message.guild.id) in modlogs:
                    modlog = modlogs[str(ctx.message.guild.id)]
                    modlog = discord.utils.get(ctx.guild.text_channels, id = modlog)
                    embed = discord.Embed(
                        title = "Nuke",
                        description = f"{channel.mention} has been nuked by {ctx.message.author.mention} for {reason}.",
                        timestamp = datetime.datetime.utcnow(),
                        color = self.blurple
                    )
                    await modlog.send(embed = embed)
        except:
            embed = discord.Embed(
                title = "Nuke Error",
                description = "I could not perform this command, I do not have the correct permissions, make sure to give me all of [these](https://github.com/xPolar/WumpusMod/blob/master/README.md#required-permissions) permissions!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def modlog(self, ctx, channel : discord.TextChannel = None):
        """
        Set the modlog.
        """
        if channel == None:
            embed = discord.Embed(
                title = "Modlog Error",
                description = "Please specify a channel!",
                color = self.errorcolor
            )
            await ctx.send(embed = embed)
        else:
            with open(r"PATHHERE\WumpusMod\Data\modlogs.json", "r") as f:
                modlogs = json.load(f)
            modlogs[str(ctx.guild.id)] = channel.id
            embed = discord.Embed(
                title = "Modlog",
                description = f"{ctx.message.guild}'s modlog is  now {channel.mention}",
                color = self.blurple
            )
            await ctx.send(embed = embed)

            with open(r"PATHHERE\WumpusMod\Data\modlogs.json", "w") as f:
                json.dump(modlogs, f, indent = 4)

def setup(bot):
    bot.add_cog(moderation(bot))
