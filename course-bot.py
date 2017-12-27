# -*- coding: utf-8 -*-
import os
import configparser

import discord
import asyncio

__version__ = '0.01.01'

# Parsing settings.cfg
config = configparser.ConfigParser()

config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.cfg"))

discord_username = config.get('Discord', 'Username') or ''
discord_token = config.get('Discord', 'Token') or ''

bot_nickname = config.get('Bot', 'Nickname') or "Discord Course Bot"
bot_status = config.get('Bot', 'Status') or "Writting Game Log"

trigger = config.get('Bot', 'Trigger') or '/cast '

# Init Discord Client
client = discord.Client()


def show_help(message, keyword, args):
    ''' Show all commands or help descrition of single command
    '''
    global cmd_table
    if len(args) > 0:
        if args[0] in cmd_table.keys():
            return client.send_message(message.channel, "%s:\t%s" % (args[0], cmd_table[args[0]]['desc']))
    msg = []
    for cmd in cmd_table.keys():
        msg.append("%s:\t%s" % (cmd, cmd_table[cmd]['desc']))
    return client.send_message(message.channel, "\n".join(msg))


def show_version(message, keyword, args):
    ''' Show version number of Discord Course Bot
    '''
    return client.send_message(message.channel, u"%s 目前的版本為(%s)" % (bot_nickname, __version__))


cmd_table = {
    'help': {
        'desc': u'顯示所有可以使用的指令。',
        'func': show_help
    },
    'version': {
        'desc': u'顯示目前的版本。',
        'func': show_version
    }
}


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
    global trigger, cmd_table

    if message.content.startswith(trigger):
        tokens = message.content[len(trigger):].split()
        command = tokens[0] or ''
        if command in cmd_table.keys():
            cmd_obj = cmd_table[command]
            await cmd_obj['func'](message, command, tokens[1:])
        else:
            await client.send_message(message.channel, u'用疑惑的眼神看著你...？ 請用 %s help 查詢指令' % trigger)


client.run(discord_token)
