import time, discord, random, json, shutil, datetime, os, logging
from discord.ext import commands
from colorama import *

os.system('cls')

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

center = shutil.get_terminal_size().columns

date = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")

config = {
    "token":"",
    "prefix":"",
    "name":"Ghostface Ticket Bot",
    "creator":"@sacrifice.shop",
    "owner_id":"",
    "support_id":""
}

banner = f"""
  ▄████  ██░ ██  ▒█████    ██████ ▄▄▄█████▓  █████▒▄▄▄       ▄████▄  ▓█████ 
 ██▒ ▀█▒▓██░ ██▒▒██▒  ██▒▒██    ▒ ▓  ██▒ ▓▒▓██   ▒▒████▄    ▒██▀ ▀█  ▓█   ▀ 
▒██░▄▄▄░▒██▀▀██░▒██░  ██▒░ ▓██▄   ▒ ▓██░ ▒░▒████ ░▒██  ▀█▄  ▒▓█    ▄ ▒███   
░▓█  ██▓░▓█ ░██ ▒██   ██░  ▒   ██▒░ ▓██▓ ░ ░▓█▒  ░░██▄▄▄▄██ ▒▓▓▄ ▄██▒▒▓█  ▄ 
░▒▓███▀▒░▓█▒░██▓░ ████▓▒░▒██████▒▒  ▒██▒ ░ ░▒█░    ▓█   ▓██▒▒ ▓███▀ ░░▒████▒
 ░▒   ▒  ▒ ░░▒░▒░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░  ▒ ░░    ▒ ░    ▒▒   ▓▒█░░ ░▒ ▒  ░░░ ▒░ ░
  ░   ░  ▒ ░▒░ ░  ░ ▒ ▒░ ░ ░▒  ░ ░    ░     ░       ▒   ▒▒ ░  ░  ▒    ░ ░  ░
░ ░   ░  ░  ░░ ░░ ░ ░ ▒  ░  ░  ░    ░       ░ ░     ░   ▒   ░           ░   
      ░  ░  ░  ░    ░ ░        ░                        ░  ░░ ░         ░  ░
                                                            ░               
                                                            
Created by: @sacrifice.zip"""

logging.getLogger('discord.client').setLevel(logging.WARNING)
logging.getLogger('discord.gateway').setLevel(logging.WARNING)

@bot.event
async def on_ready():
    for line in banner.splitlines():
        os.system(f'title Ghostface Ticket Bot {datetime.datetime.now().strftime((f"%Y-%m-%d %I:%M %p"))}')
        print(Fore.RED + line.center(center) + Fore.RESET)
        print('\033[?25l', end="")

@bot.event
async def on_member_join(member):
    
    role_name = "Members"
    
    role = discord.utils.get(member.guild.roles, name=role_name)

    
    await member.add_roles(role)
        
    with open('db/database.json', 'r') as f:
        data = json.load(f)

    if str(member.id) not in data['open']:
        data['open'][str(member.id)] = False

        with open('db/database.json', 'w') as f:
            json.dump(data, f, indent=4)


@bot.command()
async def create(ctx):
    author_id = str(ctx.author.id)
    guild = ctx.guild

    with open('db/database.json', 'r') as f:
        data = json.load(f)

    if author_id in data['open'] and not data['open'][author_id]:
        data['open'][author_id] = True

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True)
        }
        channel = await guild.create_text_channel(f"ticket-{author_id}", overwrites=overwrites)

        embed = discord.Embed(
            title=config['name'],
            description=f"<@{author_id}> ticket has successfully been created.",
            color=0x000001
        )
        embed.set_footer(text=f"{config['name']} | Created by: {config['creator']}")

        await ctx.message.reply(embed=embed)
        
        channel_embed = discord.Embed(
            title=f"{config['name']}",
            description=f"<@&{config['support_id']}> Ticket has been made.",
            color = 0x000001
        )
        channel_embed.add_field(name="", value=f"<@{author_id}> Please be patient until our support team can respond to your ticket. If you have an issue or order please give us a breif description on whats going on!")
        
        await channel.send(embed=channel_embed)
        
        with open('db/database.json', 'w') as f:
            json.dump(data, f, indent=4)
    else:
        
        embed = discord.Embed(
            title=config['name'],
            description=f"<@{author_id}> you already have an ongoing ticket.",
            color=0x000001
        )
        embed.set_footer(text=f"{config['name']} | Created by: {config['creator']}")

        await ctx.message.reply(embed=embed)

@bot.command()
async def close(ctx):
    author_id = str(ctx.author.id)
    guild = ctx.guild
    
    with open('db/database.json', 'r') as f:
        data = json.load(f)
        
    if author_id in data['open'] and data['open'][author_id]:
        
        try:
            channel_name = f"ticket-{author_id}"
            channel = discord.utils.get(guild.channels, name=channel_name)
            
            if channel:
                await channel.delete()
                data['open'][author_id] = False
                
                with open('db/database.json', 'w') as f:
                    json.dump(data, f, indent=4)
            else:
                embed = discord.Embed(
                    title=config['name'],
                    description=f"<@{author_id}> You have no open tickets.",
                    color=0x000001
                )
                embed.set_footer(text=f"{config['name']} | Created by: {config['creator']}")
                
                await ctx.message.reply(embed=embed)
        except Exception as e:
            with open('failed/error.txt', 'w') as f:
                f.write(f"{date}\n{author_id}:\n{e}")  

bot.run(config['token'])
