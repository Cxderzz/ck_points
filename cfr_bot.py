import os
from discord.ext import commands
import discord
from dotenv import load_dotenv
import json
import collections

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix=';')

@bot.event
async def on_ready():
    print('logged in as:')
    print(f'name: {bot.user.name}')
    print(f'id: {bot.user.id}')
    print('------')

@bot.listen('on_message')
async def msg_listener(message):
    if message.author == bot.user:
        return
    with open('points.JSON') as data:
        points = json.load(data)
        points = collections.Counter(points)
    if 'thanks' in message.content.lower():
        if len(message.mentions) >= 1:
            if str(message.author) != str(message.mentions[0]):
                await message.channel.send(embed=discord.Embed(title='Thanks received!', colour=discord.Color.green(),type='rich',description=f'User {message.author.mention} has thanked {message.mentions[0].mention}!',inline=True,))
                points = collections.Counter(points)
                points[str(message.mentions[0])] += 100
                points[str(message.author)] += 20
                with open('points.JSON', 'w') as jfile:
                    json.dump(dict(points),jfile)
            else:
                await message.channel.send(embed=discord.Embed(title='Error', colour=discord.Color.red(),type='rich',description='You can\'t thank yourself!', inline=True,))
    elif (';p' not in message.content.lower()) and (';l' not in message.content.lower()):
        points = collections.Counter(points)
        points[str(message.author)] += 1
        with open('points.JSON', 'w') as jfile:
            json.dump(dict(points), jfile)


@bot.command(name='p')
async def points_command(ctx, user: discord.User=None):
    with open('points.JSON') as data:
        points = json.load(data)
    if user:
        if str(user) in points.keys():
            await ctx.message.channel.send(embed=discord.Embed(colour=discord.Color.blurple(),type='rich',description=f'User {user.mention} has {points[str(user)]} points!', inline=True))
        else:
            await ctx.message.channel.send(embed=discord.Embed(title='Error', colour=discord.Color.red(),type='rich',description=f'User {user.mention} has no points.',inline=True,))
    else:
        if str(ctx.message.author) in points.keys():
            await ctx.message.channel.send(embed=discord.Embed(colour=discord.Color.blurple(),type='rich',description=f'User {ctx.message.author.mention} has {points[str(ctx.message.author)]} points!',inline=True,))
        else:
            await ctx.message.channel.send(embed=discord.Embed(title='Error', colour=discord.Color.red(),type='rich',description=f'User {ctx.message.author.mention} has no points.', inline=True,))

@bot.command(name='l')
async def leaderboard_command(ctx, amt_users: int=10):
    with open('points.JSON', 'r') as data:
        points = collections.Counter(json.load(data))
    if len(points) > 0:
        desc = ''.join(f'{index}. {username[:-5]}: {points}\n' for index, (username,points) in enumerate(points.most_common(amt_users),1))
    else:
        desc = 'There are no results to show.'
    await ctx.message.channel.send(embed=discord.Embed(title='Leaderboard', colour=discord.Color.blurple(),type='rich',description=desc,inline=True,))

@bot.command(name='rm_points')
async def rm_points(ctx, user:discord.User=None, amt:int=None):
    with open('points.JSON', 'r') as data:
        points = collections.Counter(json.load(data))
    if user and amt:
        points[str(user)] -= amt
        await ctx.channel.send(embed=discord.Embed(colour=discord.Color.green(),type='rich',description=f"Removed {amt} points from {user.mention}."))
    with open('points.JSON', 'w') as jfile:
        json.dump(dict(points), jfile)
bot.run(TOKEN)