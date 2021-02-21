import random
import discord
import requests
import os

from dotenv import load_dotenv

from animeApi import *
from cardsCore import *

client = discord.Client()
load_dotenv()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('-hello'):
        await message.channel.send(message.author.mention + ' Hello!')

    if message.content.startswith('-apiStatistics'):

        statistics = getStatistics()

        if not statistics:
            embed = discord.Embed(
                title='Statistics command error', description='An error has ocurred, please try again.', color=0xfc2803)
            await message.channel.send(embed=embed)

        else:
            statistics = statistics.json()

            embed = discord.Embed(
                title='Anilist API Statistics', color=0xf56c42)
            embed.add_field(name='Last character found', value='#'+str(statistics['data']['Character']['id'])+' - '+str(
                statistics['data']['Character']['name']['full']), inline=False)
            embed.add_field(name='Last Anime found', value='#'+str(statistics['data']['Anime']['id'])+' - '+str(
                statistics['data']['Anime']['title']['romaji']), inline=False)
            embed.add_field(name='Last Manga found', value='#'+str(statistics['data']['Manga']['id'])+' - '+str(
                statistics['data']['Manga']['title']['romaji']), inline=False)
            embed.add_field(name='Total Characters', value=str(
                statistics['data']['SiteStatistics']['characters']['nodes'][-1]['count']), inline=True)
            embed.add_field(name='Total Animes', value=str(
                statistics['data']['SiteStatistics']['anime']['nodes'][-1]['count']), inline=True)
            embed.add_field(name='Total Mangas', value=str(
                statistics['data']['SiteStatistics']['manga']['nodes'][-1]['count']), inline=True)

            await message.channel.send(embed=embed)

    if message.content.startswith('-pull'):

        i = 0
        attemps = 0
        characters = []

        while i < 3:
            character = getCharacter(random.randint(0, 72492))
            if not character:
                if attemps == 10:
                    break
                else:
                    attemps += 1
            else:
                characters.append(character.copy())
                i += 1

        if attemps != 10:
            pullImage = pullImages(characters)
            file = discord.File(pullImage, filename='pull.png')
            await message.channel.send('Here is your pull master ' + message.author.mention, file=file)
        else:
            embed = discord.Embed(
                title='Pull command error', description='An error has ocurred, please try again.', color=0xfc2803)
            await message.channel.send(embed=embed)

client.run(os.getenv('TOKEN'))
