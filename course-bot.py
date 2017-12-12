import os
import configparser

import discord
import asyncio

# Parsing settings.cfg
config = configparser.ConfigParser()

config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.cfg"))

discord_username = config.get('Discord', 'Username') or ''
discord_token = config.get('Discord', 'Token') or ''

bot_nickname = config.get('Bot', 'Nickname') or "Discord Course Bot"
bot_status = config.get('Bot', 'Status') or "Writting Game Log"

trigger = config.get('Bot', 'trigger') or '/cast'

# Init Discord Client
client = discord.Client()


@client.event
async def on_ready():
    global discord_username
    global bot_nickname
    global bot_status

    print('Discord Chat Bot Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    # Update bot nickname and status
    await client.change_nickname(member=discord.utils.find(lambda m: m.name == 'course-bot', client.get_all_members()), nickname=bot_nickname)
    await client.change_presence(game=discord.Game(name=bot_status))


@client.event
async def on_message(message):
    global trigger

    if message.content.startswith(trigger):
        await client.send_message(message.channel, '收到使用者指令： %s' % message.content[len(trigger):])


client.run(discord_token)
