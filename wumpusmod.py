#Imports
import asyncio
import discord
from discord.ext import commands
import config
import json

#Server side prefix thing
def get_prefix(bot, message):
    if message.guild == None:
        pass
    else:
        with open(r"PATHHERE\WumpusMod\Data\prefixes.json", "r") as f:
            prefixes = json.load(f)
        if str(message.guild.id) not in prefixes:
            return commands.when_mentioned_or("w!")(bot, message)
        else:
            prefix = prefixes[str(message.guild.id)]
            return commands.when_mentioned_or(prefix)(bot, message)

#Set prefix and set case sensitive to false
bot = commands.Bot(command_prefix = get_prefix, case_insensitive = True)

#Remove default help command
bot.remove_command('help')

#Cogs
cogs = ["cogs.moderation",
        "cogs.ticket_system",
        "cogs.other",
        "cogs.general"]

#Values
errorcolor = 0xFF2B2B
blurple = 0x7289DA

#Starts all cogs
print("Starting all cogs...")
for cog in cogs:
    bot.load_extension(cog)

#Check if owner
def owner(ctx):
    return ctx.author.id == config.OWNERID

#Restarts and reloads all cogs
@bot.command()
@commands.check(owner)
async def restart(ctx):
    """
    Used to restart bot
    """
    print("\nRestarting...")
    restarting = discord.Embed(
        title = "Restarting...",
        color = blurple
    )
    msg = await ctx.send(embed = restarting)
    for cog in cogs:
        bot.reload_extension(cog)
        restarting.add_field(name = f"{cog}", value = "🔁 Restarted!")
        await msg.edit(embed = restarting)
    print("All cogs loaded.\nRestarting the bot...")
    await bot.change_presence(activity = discord.Game(f"w!help | Moderating {(len(bot.users))} users!"))
    print(f"Restarted succesfully!\nServer Count - {len(bot.guilds)}\nUser Count - {len(bot.users)}")
    await asyncio.sleep(3)
    await msg.delete()
    await ctx.message.delete()

#Command error
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        errorembed = discord.Embed(
            title = f"{ctx.invoked_with} is not a command!",
            color = errorcolor
        )
        await ctx.send(embed = errorembed)
    else:
        raise error

#On ready
@bot.event
async def on_ready():
    print("All cogs loaded.")
    await bot.change_presence(activity = discord.Game(f"w!help | Moderating {(len(bot.users))} users!"))
    print(f"The bot has been started!\nServer Count - {len(bot.guilds)}\nUser Count - {len(bot.users)}")

#Starts bot
bot.run(config.TOKEN)
