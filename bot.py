import discord
import asyncio
from random import shuffle
from peewee import *
import time


db = SqliteDatabase('people.db')

class Player(Model):
    name = CharField()
    obj=CharField()
    role = CharField()
    side = SmallIntegerField()

    class Meta:
        database = db  





client = discord.Client()
night = False
players = {}
bomber = []
hilling = ''


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
    reqest = []
    if com in commands:
            try:
                reqest = commands[com](message,msg)
            except Exception as e:
                print(e)
                reqest = [(message.author, e)] 
    for chan, req in reqest:
        await client.send_message(chan, req)
    reqest = []
    

def test(message,content):
    return [(message.author,'test')]

def start_game(message, size):
    create_table(size)

    return [(message.channel, 'Попросите свои роли с помощью комманды s!role')]

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
    for i in range(size - int(size/3)):
        roles.append(['мирный',0])
    shuffle(roles)
    try:
        Player.drop_table()
    except Exception as e:
        print (e)
    Player.create_table()
    for role in roles:
        Player.create(name = 'name', obj = 'obj', role = role[0], side = role[1])

    '''grandma = Person.create(name= 'Grandma',role = 'mafia')
    grandma = Person.select().where(Person.name == 'Grandma L.').get()'''
    #print(Player.select().count())

def add_player(message,trash):
    global players
    
    name = str(message.author)
    name = name[:name.index('#')]
    players[name] = message.author
    empty_player = Player.select().where(Player.name == 'name').get()
    empty_player.name = name
    empty_player.obj = message.author
    empty_player.save()
    return [(message.author, empty_player.role)]

def night(message,trash):
    global night 
    global players
    night = True
    result = []
    size = Player.select().count()
    #mafia = Player.select().where(Player.side == 1).get()
    for p in Player.select().where(Player.side == 1):
        result.append((players[p.name],'выстрелите в жертву командой s!kill'))
    for p in Player.select().where(Player.role == 'дон мафии'):
        result.append((players[p.name],'проверьте горожанина командой s!check'))
    for p in Player.select().where(Player.role == 'шеф полиции'):
        result.append((players[p.name],'проверьте горожанина командой s!check'))
    for p in Player.select().where(Player.role == 'доктор'):
        result.append((players[p.name],'вылечите горожанина командой s!hill'))
    return result

def check(message,trash):
    player = Player.select().where(Player.role == message.author)
    if (player.role == 'дон мафии'):
        victim = Player.select().where(Player.name == message.content)
        if victim.role == 'шеф полиции':
            return [(message.author, 'да, он шеф полиции')]
    elif (player.role == 'шеф полиции'):
        victim = Player.select().where(Player.name == message.content)
        if victim.role == 'дон мафии':
            return [(message.author, 'да, он дон мафии')]
    
    else:
        text = 'очень смешно, твоя роль ' + player.role +' не позволяет проверять людей'
        return [(message.author, text)]

def kill(message,trash):
    global bomber
    bomber.append(message.content)
    return [(message.author, 'бам!')]

def hill(message,trash):
    global hill
    hill = message.content
    return [(message.author, 'вылечим '+ message.content)]

def day(message,trash):
    global bomber
    global hill
    


commands  = {
    'test': test,
    'mafia': start_game,
    'role': add_player,
    'night': night,
    'check':check,
    'kill': kill,
    'hill':hill,
    'day': day
    }

DISCORD_BOT_TOKEN = get_token()

client.run(DISCORD_BOT_TOKEN)

while True:
    pass