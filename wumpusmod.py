import discord
from discord.ext import commands

#Set prefix and set case sensitive to false
bot = commands.Bot(command_prefix = "w!", case_insensitive = True)

#Remove default help command
bot.remove_command('help')

#Cogs
cogs = ["cogs.moderation"]

#Values
errorcolor = 0xFF2B2B
blurple = 0x7289DA

#Starts all cogs
for cog in cogs:
    bot.load_extension(cog)
    print(f"{cog} has been loaded.")

#Check if owner
def owner(ctx):
    owner_ids = [229695200082132993]
    return ctx.author.id in owner_ids

#Restarts and reloads all cogs
@bot.command()
@commands.check(owner)
async def restart(ctx):
    restarted = discord.Embed(
        title = "Restart Completed!",
        color = blurple
    )
    for cog in cogs:
        print(f"Restarting {cog}")
        bot.reload_extension(cog)
    await ctx.send(embed = restarted, delete_after = 10.0)

#Command error
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        errorembed = discord.Embed(
            title = f"{ctx.message.content} is not a command!",
            color = errorcolor
        )
        await ctx.send(embed = errorembed)
    elif isinstance(error, commands.MissingPermissions):
        return
    else:
        raise error

#Starts bot
bot.run("NTk2NTMyNzQ0MjE4MjE0NDAy.XR66bw.k8cb5coY7bP1Hr7vzf-dc9RIN4g")
