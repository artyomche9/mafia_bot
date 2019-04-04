import discord
import asyncio
from random import shuffle
from peewee import *


db = SqliteDatabase('people.db')

class Player(Model):
    name = CharField()
    obj=CharField()
    role = CharField()
    side = SmallIntegerField()

    class Meta:
        database = db  # модель будет использовать базу данных 'people.db'




client = discord.Client()
mess = ''


def get_token():
    f = open('token.bin','r')
    return f.read()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    msg = str(message.content)
    if msg.startswith('s!'):
        if '.' in msg:
            com = msg[msg.index('!') + 1: msg.index('.')]
            msg = msg[msg.index('.') + 1:]
        else:
            com = msg[msg.index('!') + 1: ]
    else: return None
    channel = message.author
    reqest = 'error'
    if com in commands:
            try:
                channel,reqest = commands[com](message,msg)
            except Exception as e:
                print(e)
                reqest = e     
    await client.send_message(channel, reqest)

def test(message,content):
    return message.author,'test'

def start_game(message, size):
    create_table(size)

    return message.channel, 'done'

def create_table(size):
    size = int(size)
    roles = []
    if size >= 6:
        size -= 3
        roles.append(['дон мафии',1])
        roles.append(['шеф полиции',0])
        roles.append(['доктор',0])
    for i in range(int(size/3)):
        roles.append(['мафия',1])
    for i in range(int(size - size/3)):
        roles.append(['мирный',0])
    shuffle(roles)
    Player.create_table()
    for role in roles:
        Player.create(name = 'name', obj = 'obj', role = role[0], side = role[1])

    '''grandma = Person.create(name= 'Grandma',role = 'mafia')
    grandma = Person.select().where(Person.name == 'Grandma L.').get()'''
    #print(grandma)
    

commands  = {
    'test': test,
    'mafia': start_game
    }

def is_channel(message):
    if not(str(message.channel) in channel):
        channel.append(str(message.channel))
        channels[str(message.channel)] = message.channel



DISCORD_BOT_TOKEN = get_token()

client.run(DISCORD_BOT_TOKEN)

while True:
    pass