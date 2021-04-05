import os
import discord
from dotenv import load_dotenv
import datetime
import json
import collections

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

@client.event
async def on_ready():
    print(f"{client.user} has connected to discord!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if '792803155217874964' in message.content.lower():
        return
    with open('points.JSON') as data:
        points = json.load(data)
        points = collections.Counter(points)
    if "embed please" in message.content.lower():
        await message.channel.send(embed=discord.Embed(title="This is a test embed!", colour=discord.Color.green(),type="rich",description="This is the description of the embed", time=datetime.datetime,inline=True,))
    print(message.author.id)
    if 'thanks' in message.content.lower():
        if len(message.mentions) >= 1:
            if str(message.author) != str(message.mentions[0]):
                await message.channel.send(embed=discord.Embed(title="Thanks received!", colour=discord.Color.green(),type="rich",description=f"User {message.author.mention} has thanked {message.mentions[0].mention}!", time=datetime.datetime,inline=True,))
                points = collections.Counter(points)
                points[str(message.mentions[0])] += 100
                with open('points.JSON', 'w') as jfile:
                    json.dump(dict(points),jfile)
            else:
                await message.channel.send(embed=discord.Embed(title="Error", colour=discord.Color.red(),type="rich",description="You can't thank yourself!", time=datetime.datetime,inline=True,))
        else:
            await message.channel.send(embed=discord.Embed(title="Error", colour=discord.Color.red(),type="rich",description="Make sure to thank someone the correct way! Just say: Thanks @[username]", time=datetime.datetime,inline=True,))

    if ';l' in message.content.lower():
        with open('points.JSON', 'r') as data:
            points = collections.Counter(json.load(data))
        if len(points) > 0:
            # if message.content.lower() == ";l":
            #     pl = points.most_common()
            # else:
            #     pl = points.most_common(int(message.content.lower().split()[-1]))
            desc = "".join(f"{index}. {username[:-5]}: {points}\n" for index, (username,points) in enumerate((points.most_common() if message.content.lower() == ";l" else points.most_common(int(message.content.lower().split()[-1]))),1))
            await message.channel.send(embed=discord.Embed(title="Leaderboard", colour=discord.Color.blurple(),type='rich',description=desc,time=datetime.datetime,inline=True,))
        else:
            await message.channel.send(embed=discord.Embed(title="Leaderboard", colour=discord.Color.blurple(),description="There are no results to show.", type="rich", time=datetime.datetime,inline=True))
    if ";p" == message.content.lower():
        with open('points.JSON') as data:
            points = json.load(data)
        print(points)
        if len(message.mentions) == 1:
            if str(message.mentions[0]) in points.keys():
                await message.channel.send(embed=discord.Embed(title="Success!", colour=discord.Color.green(),type="rich",description=f"User {message.mentions[0].mention} has {points[str(message.mentions[0])]} points!", time=datetime.datetime,inline=True,))
            else:
                await message.channel.send(embed=discord.Embed(title="Error", colour=discord.Color.red(),type="rich",description=f"User {message.mentions[0].mention} has no points.", time=datetime.datetime,inline=True,))
        else:
            if str(message.author) in points.keys():
                await message.channel.send(embed=discord.Embed(title="Success!", colour=discord.Color.green(),type="rich",description=f"User {message.author.mention} has {points[str(message.author)]} points!", time=datetime.datetime,inline=True,))
            else:
                print(points.keys())
                await message.channel.send(embed=discord.Embed(title="Error", colour=discord.Color.red(),type="rich",description=f"User {message.author.mention} has no points.", time=datetime.datetime,inline=True,))

client.run(TOKEN)
