import asyncio
import json
import random

import gtts
from discord.ext import commands
import discord
import requests
import apiai

GOOGLE_TOKEN = "ce5730449289451e83d5df8aece17558"
IS_ANGRY = False
IS_TALKING = False
token = "NjcwNzA4NzUwNzM4MjYwMDIw.Xi3mCw.CU6uW6L011D6YHD5rfn6v2IxG_w"
bot = commands.Bot(command_prefix='$')
LANG = 'uk'
SLOW = False
GUILD: discord.Guild = None
TEXT_CHAN = None
HELP = "команды:\n" \
       "Join, leave\n" \
       "langs - список доступных языков\n" \
       "init - инициализация\n" \
       "getLang - текущий язык/n" \
       "setLang - учтановить язык \n" \
       "isSlow, setIsSlow\n" \
       "hate , hateEveryone, hateRand, hateMe\n" \
       "play текст - озвучить текст\n" \
       "префикс - $ ($play, $hate, ...)"
LAST_MEMBER = None
songs = [{
    "text": "Много лет прошло с тех пор,\n"
            "Когда в Союз проник раскол\nС перестройкой подло влился\nКогда занавес открылся\nЗапад облетела птица\nКровожадная орлица\nНо пришел Владимир Путин\nИ сказал — жить лучше будет!\nВладимир Путин молодец,\nПолитик лидер и борец,\nНаш президент страну поднял,\nРоссию Путин не предал.\nВ новый век вошла Россия\nИ вздохнула с новой силой\nКурс взяла на возрожденье\nПосле божьего забвенья\nЕврозапад взбеленился,\nГрязной ложью навалился,\nВежливо ответил Путин —\nНас не трогать, мы не шутим!\nВладимир Путин молодец,\nПолитик лидер и борец,\nНаш президент страну поднял,\nРоссию Путин не предал.\nВладимир Путин молодец,\nПолитик лидер и борец,\nНаш президент страну поднял,\nРоссию Путин не предал.\nВладимир Путин молодец,\nПолитик лидер и борец,\nНаш президент страну поднял,\nРоссию Путин не предал.\nРоссию Путин не предал.\nСлава России.",
    "lang": "ru"
},
    {
        "text": "Ще не вмерли, Україно,\n"
                "І слава, і воля!\nЩе нам, браття-молодці,\nУсміхнеться доля!\nЗгинуть наші вороги,\nЯк роса на сонці;\nЗапануєм, браття й ми\nУ своїй сторонці.\n\nПриспів:\n\nДушу, тіло ми положим\nЗа свою свободу\nІ покажем, що ми браття\nКозацького роду.\nГей-гей, браття миле,\nНумо братися за діло!\nГей-гей пора встати,\nПора волю добувати!\n\nНаливайко, Залізняк\nІ Тарас Трясило\nКличуть нас із-за могил\nНа святеє діло.\nІзгадаймо славну смерть\nЛицарства-козацтва,\nЩоб не втратить марне нам\nСвоєго юнацтва.\n\nПриспів.\n\nОй, Богдане, Богдане,\nСлавний наш гетьмане!\nНа-що віддав Україну\nМоскалям поганим?!\nЩоб вернути її честь,\nЛяжем головами,\nНазовемся України\nВірними синами!\n\nПриспів.\n\nНаші браття слов’яни\nВже за зброю взялись;\nНе діжде ніхто, щоб ми\nПо-заду зістались.\nПоєднаймось разом всі,\nБратчики-славяне:\nНехай гинуть вороги,\nНай воля настане!\n\nПриспів.",
        "lang": "uk"
    }
]


async def hate_rand():
    try:
        global LAST_MEMBER
        print("hate")
        member: discord.Member = random.choice(GUILD.members)
        await TEXT_CHAN.send(f'сегодня хейтим {member.display_name}')
        role = discord.utils.get(GUILD.roles, name="пидр")
        try:
            # noinspection PyUnboundLocalVariable
            await LAST_MEMBER.remove_roles(role)
        except Exception as e:
            print(e)
        LAST_MEMBER = member
        await member.add_roles(role)
    except Exception as e:
        print(e)


async def bc():
    await bot.wait_until_ready()
    while True:
        print("h")
        await asyncio.sleep(random.randint(100, 10000))
        await hate_rand()


@bot.command()
async def langs(ctx):
    with open('langs') as f:
        s = ""
        for i in range(51):
            s += f.readline()
    await ctx.send(s)


@bot.command()
async def sing(ctx):
    try:
        chan = ctx.message.author.voice.channel
        await chan.connect()
        await ctx.send("на месте")
    except:
        pass
    song = random.choice(songs)
    await play(ctx, song['text'], language=song['lang'])


@bot.command()
async def slava(ctx):
    try:
        chan = ctx.message.author.voice.channel
        await chan.connect()
        await ctx.send("на месте")
    except:
        pass
    await play(ctx, "слава Україні! Героям слава!"
                    "слава Україні! Героям слава!"
                    "слава Україні! Героям слава!"
                    "слава Україні! Героям слава!"
                    "слава Україні! Героям слава!"
                    "слава Україні! Героям слава!"
                    "слава Україні! Героям слава!"
                    "слава Україні! Героям слава!"
                    "слава Україні! Героям слава!"
                    "слава Україні! Героям слава!"
                    "слава Україні! Героям слава!"
                    "слава Україні! Героям слава!"
                    "слава Україні! Героям слава!"
                    "слава Україні! Героям слава!"
                    "слава Україні! Героям слава!"
                    "слава Україні! Героям слава!"
               )


@bot.command()
async def init(ctx: commands.Context, language=LANG, slow=SLOW):
    global GUILD
    global TEXT_CHAN
    global LANG
    global Slow
    SLOW = slow
    GUILD = ctx.guild
    TEXT_CHAN = ctx.channel
    LANG = language
    await ctx.send(f'текущий язык: {LANG}')
    await ctx.send(f'текущая скорость: {SLOW}')
    await ctx.send(f'id сервера {GUILD.id}')
    await ctx.send(f'id канала {TEXT_CHAN.id}')
    await ctx.send(HELP)


@bot.command()
async def getLang(ctx: commands.Context):
    await ctx.send(LANG)


@bot.command()
async def test(ctx):
    await TEXT_CHAN.send()


@bot.command()
async def setLang(ctx: commands.Context, lang):
    global LANG
    LANG = lang


@bot.command()
async def setIsSlow(ctx: commands.Context, slow):
    global SLOW
    SLOW = slow


@bot.command()
async def isSlow(ctx: commands.Context):
    global SLOW
    await ctx.send(SLOW)


@bot.command()
async def hate(ctx, member: discord.Member, reason="он пидр", language=LANG, slow=SLOW):
    await ctx.channel.purge(limit=1)
    try:
        chan = ctx.message.author.voice.channel
        await chan.connect()
        print("connected")
    except:
        pass

    text = f'хетим {member.display_name} по причине {reason}'
    await ctx.send(text)
    if not language:
        language = LANG
    out = gtts.gTTS(text=text, lang=language, slow=slow)
    out.save('hate.mp3')
    print("done")
    audio_source = discord.FFmpegPCMAudio('hate.mp3')
    voice_client: discord.VoiceClient = bot.voice_clients[0]
    while True:
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)
            break


@bot.command()
async def hateEveryone(ctx: commands.Context, reason="клоун", language=LANG, slow=SLOW):
    await ctx.channel.purge(limit=1)
    guild: discord.Guild = ctx.guild
    members = guild.members
    for member in members:
        try:
            chan = ctx.message.author.voice.channel
            await chan.connect()
            print("connected")
        except:
            pass

        text = f'хетим {member.display_name} по причине {reason}'
        await ctx.send(text)
        if not language:
            language = LANG
        out = gtts.gTTS(text=text, lang=language, slow=slow)
        out.save('hate.mp3')
        print("done")
        audio_source = discord.FFmpegPCMAudio('hate.mp3')
        voice_client: discord.VoiceClient = bot.voice_clients[0]
        while True:
            if not voice_client.is_playing():
                voice_client.play(audio_source, after=None)
                break


@bot.command()
async def hateRand(ctx: commands.Context, reason="клоун", language=LANG, slow=SLOW):
    global LAST_MEMBER
    guild: discord.Guild = ctx.guild
    members = guild.members
    member = random.choice(members)
    role = discord.utils.get(GUILD.roles, name="пидр")
    try:
        # noinspection PyUnboundLocalVariable
        await LAST_MEMBER.remove_roles(role)
    except Exception as e:
        print(e)
    LAST_MEMBER = member
    await member.add_roles(role)
    await hate(ctx, member, reason, language, slow)


@bot.command()
async def hateMe(ctx: commands.Context, reason="клоун", language=LANG, slow=SLOW):
    member = ctx.author
    await hate(ctx, member, reason, language, slow)


@bot.command()
async def echo(ctx, arg):
    await ctx.channel.purge(limit=1)
    await ctx.send(arg)


# @bot.command()
# async def kick(ctx, person: discord.Member, *, reason="sosi"):
#     print(person)
#     print(person.display_name)
#     print(person.history())
#     print(person.status)
#     print(person.roles)
#     if person.display_name != "matvik22000":
#         await person.kick(reason=reason)
#     else:
#         await ctx.send("sam soci")


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("kickni clouna"))
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_message(msg: discord.Message):
    if msg.content[0] != "$" and msg.author.display_name != "haterBot" and IS_TALKING:
        async with msg.channel.typing():
            request = apiai.ApiAI(GOOGLE_TOKEN).text_request()  # Токен API к Dialogflow
            request.lang = 'ru'  # На каком языке будет послан запрос
            request.session_id = 'testBot'  # ID Сессии диалога (нужно, чтобы потом учить бота)
            request.query = msg.content  # Посылаем запрос к ИИ с сообщением от юзера
            response = None
        try:
            responseJson = json.loads(request.getresponse().read().decode('utf-8'))
            response = responseJson['result']['fulfillment']['speech']
        except:
            pass
        if response:
            if response == "joke":
                await joke_from_msg(msg)
            else:
                await msg.channel.send(response)
        else:
            await msg.channel.send("Иди нахуй.")
    else:
        await bot.process_commands(msg)


@bot.command(pass_context=True)
async def join(ctx):
    chan = ctx.message.author.voice.channel
    await chan.connect()


@bot.command(pass_context=True)
async def leave(ctx):
    global IS_ANGRY
    try:
        if not IS_ANGRY:
            await bot.voice_clients[0].disconnect()
        else:
            await ctx.channel.purge(limit=1)
            await ctx.send("nope")
    except Exception as e:
        print(e)
        await bot.voice_clients[0].disconnect()


@bot.command()
async def talk(ctx):
    global IS_TALKING
    IS_TALKING = not IS_TALKING
    await ctx.send(IS_TALKING)


@bot.command(pass_context=True)
async def play(ctx, arg, language=None, slow=SLOW):
    try:
        chan = ctx.message.author.voice.channel
        await chan.connect()
        await ctx.send("на месте")
    except:
        pass

    text = arg
    print("in progress")
    print(LANG)
    if not language:
        language = LANG
    print(language)
    await ctx.send("в процессе...")
    out = gtts.gTTS(text=text, lang=language, slow=slow)
    out.save('text.mp3')
    print("done")

    audio_source = discord.FFmpegPCMAudio('text.mp3')
    voice_client = bot.voice_clients[0]
    if not voice_client.is_playing():
        voice_client.play(audio_source, after=None)


async def play_from_msg(msg: discord.Message, arg, language=None, slow=SLOW):
    try:
        chan = msg.author.voice.channel
        await chan.connect()
        await msg.channel.send("на месте")
    except:
        pass

    text = arg
    print("in progress")
    print(LANG)
    if not language:
        language = LANG
    print(language)
    await msg.channel.send("в процессе...")
    out = gtts.gTTS(text=text, lang=language, slow=slow)
    out.save('text.mp3')
    print("done")

    audio_source = discord.FFmpegPCMAudio('text.mp3')
    voice_client = bot.voice_clients[0]
    if not voice_client.is_playing():
        voice_client.play(audio_source, after=None)


@bot.command()
async def joke(ctx):
    r = requests.get(url='http://anek.ws/anekdot/export8.php')
    text = r.text.replace("<br />", "")
    text = text.replace("&quot", "")
    text = text.split(">")[2].split("</")[0]
    await ctx.send(text)
    await play(ctx, text)


async def joke_from_msg(msg: discord.Message):
    r = requests.get(url='http://anek.ws/anekdot/export8.php')
    text = r.text.replace("<br />", "")
    text = text.replace("&quot", "")
    text = text.split(">")[2].split("</")[0]
    await msg.channel.send(text)
    await play_from_msg(msg, text)
g

@bot.command()
async def call(ctx):
    text = "Илья Илья, ИЛЬЯ, ИлЬя, иЛЬЯ, ИльЯ. Ильяилльяильяильяиль иииииииииииииииииииилллллллья ильяяяяя яяяяя и и  иильяяяя илья"
    await ctx.send(text)
    await play(ctx, text)


@bot.command()
async def honor(ctx):
    try:
        chan = ctx.message.author.voice.channel
        await chan.connect()
        await ctx.send("на месте")
    except:
        pass

    await ctx.send("Слава Украине!")
    audio_source = discord.FFmpegPCMAudio('himn.mp3')
    voice_client = bot.voice_clients[0]
    if not voice_client.is_playing():
        voice_client.play(audio_source, after=None)


@bot.command()
async def russia(ctx):
    try:
        chan = ctx.message.author.voice.channel
        await chan.connect()
        await ctx.send("на месте")
    except:
        pass

    await ctx.send("ВЛАДИМИР ПУТИН МОЛОДЕЦ!!!!!!!")
    audio_source = discord.FFmpegPCMAudio('VVP.mp3')
    voice_client = bot.voice_clients[0]
    if not voice_client.is_playing():
        voice_client.play(audio_source, after=None)


@bot.command()
async def rage(ctx):
    global IS_ANGRY
    IS_ANGRY = not IS_ANGRY
    await ctx.send(IS_ANGRY)


# @bot.command()
# async def env(ctx: commands.Context):
#     guild: discord.Guild = ctx.guild
#     await guild.edit(name="test")


bot.loop.create_task(bc())

bot.run(token)
