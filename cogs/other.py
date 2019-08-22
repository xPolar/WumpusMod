import asyncio
import datetime
import discord
from discord.ext import commands
import itertools
import json
from paginator import Pages
import time

class HelpPaginator(Pages):
    def __init__(self, help_command, ctx, entries, *, per_page=4):
        super().__init__(ctx, entries=entries, per_page=per_page)
        self.reaction_emojis.append(('\N{WHITE QUESTION MARK ORNAMENT}', self.show_bot_help))
        self.total = len(entries)
        self.help_command = help_command
        self.prefix = help_command.clean_prefix

    def get_bot_page(self, page):
        cog, description, commands = self.entries[page - 1]
        self.title = f'{cog} Commands'
        self.description = description
        return commands

    def prepare_embed(self, entries, page, *, first=False):
        self.embed.clear_fields()
        self.embed.description = self.description
        self.embed.title = self.title

        self.embed.set_footer(text=f'Use "{self.prefix}help [Command]" for more info on a command.')

        for entry in entries:
            signature = f'{self.prefix}{entry.qualified_name} {entry.signature}'
            self.embed.add_field(name=signature, value=entry.short_doc or "No help given", inline=False)

        if self.maximum_pages:
            self.embed.set_author(name=f'Page {page}/{self.maximum_pages} ({self.total} commands)')

    async def show_bot_help(self):
        """Shows how to use the bot"""

        self.embed.title = 'Using the bot'
        self.embed.description = 'Hello! Welcome to the help page.'
        self.embed.clear_fields()

        entries = (
            ('<argument>', 'This means the argument is __**required**__.'),
            ('[argument]', 'This means the argument is __**optional**__.'),
            ('[A|B]', 'This means the it can be __**either A or B**__.'),
            ('[argument...]', 'This means you can have multiple arguments.\n'
                              'Now that you know the basics, it should be noted that...\n'
                              '__**You do not type in the brackets!**__')
        )

        self.embed.add_field(name='How do I use this bot?', value='Reading the bot signature is pretty simple.')

        for name, value in entries:
            self.embed.add_field(name=name, value=value, inline=False)

        self.embed.set_footer(text=f'We were on page {self.current_page} before this message.')
        await self.message.edit(embed=self.embed)

        async def go_back_to_current_page():
            await asyncio.sleep(30.0)
            await self.show_current_page()

        self.bot.loop.create_task(go_back_to_current_page())


class PaginatedHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__(command_attrs={
            'cooldown': commands.Cooldown(1, 3.0, commands.BucketType.member),
            'help': 'Shows help about the bot, a command, or a category'
        })

    async def on_help_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(str(error.original))

    def get_command_signature(self, command):
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            aliases = '|'.join(command.aliases)
            fmt = f'[{command.name}|{aliases}]'
            if parent:
                fmt = f'{parent} {fmt}'
            alias = fmt
        else:
            alias = command.name if not parent else f'{parent} {command.name}'
        return f'{alias} {command.signature}'

    async def send_bot_help(self, mapping):
        def key(c):
            return c.cog_name or '\u200bBot Owner'

        bot = self.context.bot
        entries = await self.filter_commands(bot.commands, sort=True, key=key)
        nested_pages = []
        per_page = 8
        total = 0

        for cog, commands in itertools.groupby(entries, key=key):
            commands = sorted(commands, key=lambda c: c.name)
            if len(commands) == 0:
                continue

            total += len(commands)
            actual_cog = bot.get_cog(cog)
            # get the description if it exists (and the cog is valid) or return Empty embed.
            description = (actual_cog and actual_cog.description) or discord.Embed.Empty
            nested_pages.extend((cog, description, commands[i:i + per_page]) for i in range(0, len(commands), per_page))

        # a value of 1 forces the pagination session
        pages = HelpPaginator(self, self.context, nested_pages, per_page=1)

        # swap the get_page implementation to work with our nested pages.
        pages.get_page = pages.get_bot_page
        pages.total = total

        await pages.paginate()

    async def send_cog_help(self, cog):
        entries = await self.filter_commands(cog.get_commands(), sort=True)
        pages = HelpPaginator(self, self.context, entries)
        pages.title = f'{cog.qualified_name} Commands'
        pages.description = cog.description

        await pages.paginate()

    def common_command_formatting(self, page_or_embed, command):
        page_or_embed.title = self.get_command_signature(command)
        if command.description:
            page_or_embed.description = f'{command.description}\n\n{command.help}'
        else:
            page_or_embed.description = command.help or 'No help found...'

    async def send_command_help(self, command):
        # No pagination necessary for a single command.
        embed = discord.Embed(color= 0x7289DA)
        self.common_command_formatting(embed, command)
        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        subcommands = group.commands
        if len(subcommands) == 0:
            return await self.send_command_help(group)

        entries = await self.filter_commands(subcommands, sort=True)
        pages = HelpPaginator(self, self.context, entries)
        self.common_command_formatting(pages, group)

        await pages.paginate()

class Other(commands.Cog):



    def __init__(self, bot):
        self.bot = bot
        self.errorcolor = 0xFF2B2B
        self.blurple = 0x7289DA
        self.bot = bot
        self.old_help_command = bot.help_command
        bot.help_command = PaginatedHelpCommand()
        bot.help_command.cog = self
        self.color = 0x7289DA
        self.bot.launch_time = datetime.datetime.utcnow()

        def cog_unload(self):
            self.bot.help_command = self.old_help_command

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def prefix(self, ctx, *, prefix):
        """
        Set the servers prefix.
        """
        if ctx.message.author.id == ctx.guild.owner.id:
            with open(r"PATHHERE\WumpusMod\prefixes.json", "r") as f:
                prefixes = json.load(f)

            prefixes[str(ctx.guild.id)] = prefix
            embed = discord.Embed(
                title = "Prefix",
                description = f"{ctx.message.guild}'s prefix is  now `{prefix}`",
                color = self.blurple
            )
            await ctx.send(embed = embed)

            with open(r"PATHHERE\WumpusMod\prefixes.json", "w") as f:
                json.dump(prefixes, f, indent = 4)

    @prefix.error
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
        """
        Check the bots current ping.
        """
        embed = discord.Embed(
            title = f"Pong!",
            description = f"{round(self.bot.latency * 1000)} ms",
            color = self.blurple
        )
        await ctx.send(embed = embed)

    #Github command
    @commands.command()
    async def github(self, ctx):
        """
        Get a link to the github.
        """
        embed = discord.Embed(
            title = f"Feel free to check out the github!",
            url = "https://github.com/xPolar/WumpusMod",
            color = self.blurple
        )
        await ctx.send(embed = embed)

    #Support command
    @commands.command()
    async def support(self, ctx):
        """
        Get a link to the support server.
        """
        embed = discord.Embed(
            title = f"Feel free to join our support server!",
            url = "https://discord.gg/gkAKatd",
            color = self.blurple
        )
        await ctx.send(embed = embed)

    #Invite command
    @commands.command()
    async def invite(self, ctx):
        """
        Get a link to invite the bot.
        """
        embed = discord.Embed(
            title = f"Feel free to invite me!",
            url = "https://discordapp.com/api/oauth2/authorize?client_id=596532744218214402&permissions=8&scope=bot",
            color = self.blurple
        )
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Other(bot))
