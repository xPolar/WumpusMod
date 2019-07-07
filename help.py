import discord
from discord.ext import commands

class help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.errorcolor = 0xFF2B2B
        self.blurple = 0x7289DA

    @commands.command()
    async def help(self, ctx, module = None):
        if module == None:
            embed = discord.Embed(
                title = "``Moderation``",
                description = "6 total commands.",
                color = self.blurple
            )
            embed.set_author(name = "Categorys")
            embed.add_field(name = "``Tickets``", value = "5 total commands.")
            embed.set_footer(text = "For more information on each category do !help (Category).")
            await ctx.send(embed = embed)
        else:
            if module.lower() == "moderation":
                embed = discord.Embed(
                    title = "Commands",
                    description = "**Purge / Clear** - Deletes a large amount of messages.\n**Kick** - Kicks a user from the server.\n**Ban** - Bans a user from the server.\n**Unban** - Unbans a user from the server.\n**Mute** - Mutes a user so they can't talk\n**Unmute** - Unmutes a user so they can talk.",
                    color = self.blurple
                )
                embed.set_author(name = "Moderation")
                embed.set_footer(text = "For more information on each command do !help (Command).")
                await ctx.send(embed = embed)
            if module.lower() == "tickets":
                embed = discord.Embed(
                    title = "Commands",
                    description = "**Ticket** - Creates a new ticket.\n**Adduser** - Adds a user to a ticket.\n**Removeuser / Rmuser** - Removes a user from a ticket.\n**Close** - Closes a ticket.\n**Supporteradd** - Adds a user to the supporter role.",
                    color = self.blurple
                )
                embed.set_author(name = "Tickets")
                embed.set_footer(text = "For more information on each command do !help (Command).")
                await ctx.send(embed = embed)
            if module.lower() == "purge" or "clear":
                embed = discord.Embed(
                    title = "Description",
                    description = "Removes a large amount of messages in a channel.",
                    color = self.blurple
                )
                embed.set_author(name = "Purge / Clear")
                embed.add_field(name = "Usage", value = "``w!purge (Amount)``\n``w!clear (Amount)``")
                await ctx.send(embed = embed)
            if module.lower() == "kick":
                embed = discord.Embed(
                    title = "Description",
                    description = "Kicks a user from the server.",
                    color = self.blurple
                )
                embed.set_author(name = "Kick")
                embed.add_field(name = "Usage", value = "``w!kick (User) (Reason)``")
                await ctx.send(embed = embed)
            if module.lower() == "ban":
                embed = discord.Embed(
                    title = "Description",
                    description = "Bans a user from the server.",
                    color = self.blurple
                )
                embed.set_author(name = "Ban")
                embed.add_field(name = "Usage", value = "``w!ban (User) (Reason)``")
                await ctx.send(embed = embed)
            if module.lower() == "unban":
                embed = discord.Embed(
                    title = "Description",
                    description = "Unbans a user from the server.",
                    color = self.blurple
                )
                embed.set_author(name = "Unban")
                embed.add_field(name = "Usage", value = "``w!unban (User)``")
                await ctx.send(embed = embed)
            if module.lower() == "mute":
                embed = discord.Embed(
                    title = "Description",
                    description = "Mutes a user so they can't talk.",
                    color = self.blurple
                )
                embed.set_author(name = "Mute")
                embed.add_field(name = "Usage", value = "``w!mute (User) (Reason)``")
                await ctx.send(embed = embed)
            if module.lower() == "unmute":
                embed = discord.Embed(
                    title = "Description",
                    description = "Unmutes a user so they can talk.",
                    color = self.blurple
                )
                embed.set_author(name = "Unmute")
                embed.add_field(name = "Usage", value = "``w!unmute (User)``")
                await ctx.send(embed = embed)
            if module.lower() == "ticket":
                embed = discord.Embed(
                    title = "Description",
                    description = "Creates a new ticket.",
                    color = self.blurple
                )
                embed.set_author(name = "Ticket")
                embed.add_field(name = "Usage", value = "``w!ticket (Reason)``")
                await ctx.send(embed = embed)
            if module.lower() == "close":
                embed = discord.Embed(
                    title = "Description",
                    description = "Closes a ticket.",
                    color = self.blurple
                )
                embed.set_author(name = "Close")
                embed.add_field(name = "Usage", value = "``w!close``")
                await ctx.send(embed = embed)
            if module.lower() == "adduser":
                embed = discord.Embed(
                    title = "Description",
                    description = "Adds a user to a ticket.",
                    color = self.blurple
                )
                embed.set_author(name = "Adduser")
                embed.add_field(name = "Usage", value = "``w!adduser (User)``")
                await ctx.send(embed = embed)
            if module.lower() == "removeuser" or "rmuser":
                embed = discord.Embed(
                    title = "Description",
                    description = "Removes a user from a ticket.",
                    color = self.blurple
                )
                embed.set_author(name = "Removeuser / Rmuser")
                embed.add_field(name = "Usage", value = "``w!removemuser (User)``\n``w!rmuser (User)``")
                await ctx.send(embed = embed)
            if module.lower() == "supporteradd":
                embed = discord.Embed(
                    title = "Description",
                    description = "Adds a user to the supporter role.",
                    color = self.blurple
                )
                embed.set_author(name = "Supporteradd")
                embed.add_field(name = "Usage", value = "``w!supporteradd (User)``")
                await ctx.send(embed = embed)
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

def setup(bot):
    bot.add_cog(help(bot))
