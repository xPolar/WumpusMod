import discord
from discord.ext import commands
import asyncio

#Set prefix and set case sensitive to false
bot = commands.Bot(command_prefix = "w!", case_insensitive = True)

#Remove default help command
bot.remove_command('help')

#Cogs
cogs = ["cogs.moderation",
        "cogs.tickets",
        "cogs.other",]

#Values
errorcolor = 0xFF2B2B
blurple = 0x7289DA

#Starts all cogs
for cog in cogs:
    bot.load_extension(cog)

#Check if owner
def owner(ctx):
    return ctx.author.id == OWNERID

#Restarts and reloads all cogs
@bot.command()
@commands.check(owner)
async def restart(ctx):
    restarted = discord.Embed(
        title = "Restart Completed!",
        color = blurple
    )
    for cog in cogs:
        bot.reload_extension(cog)
    await ctx.message.delete()
    await bot.change_presence(activity = discord.Game(f"w!help | Moderating {(len(bot.users))} users!"))
    print("\nReloading all cogs...")
    await asyncio.sleep(3)
    print("All cogs loaded.\nRestarting the bot...")
    await asyncio.sleep(3)
    print(f"Restarted succesfully!\nServer Count - {len(bot.guilds)}\nUser Count - {len(bot.users)}")
    await ctx.send(embed = restarted, delete_after = 5.0)

#Command error
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        errorembed = discord.Embed(
            title = f"{ctx.invoked_with} is not a command!",
            color = errorcolor
        )
        await ctx.send(embed = errorembed)
    elif isinstance(error, commands.MissingPermissions):
        channel = bot.get_channel(ERRORLOGGINGCHANNELID)
        embed = discord.Embed(
            title = "Invokation",
            description = ctx.message.content,
            color = errorcolor
        )
        embed.set_author(name = "Error")
        embed.add_field(name = "Result", value = error)
        await channel.send(embed = embed)
        return
    else:
        raise error

#On ready
@bot.event
async def on_ready():
    print("Loading all cogs...")
    await asyncio.sleep(3)
    print("All cogs loaded.\nStarting the bot...")
    await asyncio.sleep(3)
    await bot.change_presence(activity = discord.Game(f"w!help | Moderating {(len(bot.users))} users!"))
    print(f"The bot has been started!\nServer Count - {len(bot.guilds)}\nUser Count - {len(bot.users)}")

#Starts bot
bot.run("TOKEN")
