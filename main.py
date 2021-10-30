import requests
import discord
import json
import os
from dotenv import load_dotenv
from osrsbox import items_api

url = 'http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item='

items = items_api.load()

load_dotenv()
client = discord.Client()


def getItemPrice(itemId):
    try:
        response = requests.get(url + itemId)
    except Exception as e:
        print(e)
    try:
        msg = response.json()['item']['name'] + ': ' + str(response.json()['item']['current']['price'])
        return msg
    except Exception as e:
        print(e)
        return ''

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content
    if msg.startswith('!price'):
        itemName = ''
        for word in msg.split():
            if word != '!price':
                itemName += (word + ' ')
        if itemName != '':
            itemName = itemName[:-1]
            for item in items:
                if item.name.casefold() == itemName.casefold():
                    price = getItemPrice(f'{item.id}')
                    if price != '':
                        await message.channel.send(price + ' gp')
                    else:
                        await message.channel.send(f'{itemName}' + ' is not tradeable')
                    return
            await message.channel.send('Could not find item: ' + f'{itemName}')
    

client.run(os.getenv('TOKEN'))
