##Alex Trebot

import os, discord, random, dotenv, selenium, asyncio, youtube_dl, ffmpeg, queue 
import time;

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.support.ui import WebDriverWait
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from dotenv import load_dotenv
from youtube_dl import YoutubeDL

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='*', case_insensitive=True, intents=intents)

ydl_opts = {'format': 'bestaudio', 'noplaylist':'True'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

mover = [
         
         797116172667322408, #FinnTheHuman
         133782443495915520, #Bruffn
         162318341589958656, #LarlosCopez
         190974199815208961, #Liam O'Hagan
         164205353330802688, #Morgan Westgarth
         802703737529040916, #alimac
         802708014234337280, #alimac
         802691698790105109, #anirtak
         650570885593563159, #authenticali
         533443932898459668, #CassidyJade
         802630951539834940, #Eric Di Gravio
         133692542146445312, #Ethan
         225002698712416256, #Jake 'n Bake
         689864999312818194, #rebecca.childs
         156242684929900545, #toolmantyler
         152203564658327561, #TY DE
         803277011005997056, #AlexTreBOT
         170712800082132992, #Monty
         
    ]

nope = [
        'Sorry, I don\'t take orders from you.',
        'Alas, such a task is no match for my incompetency.',
        'Sorry. Coffee break.',
        'Could you try asking later?',
        'Is there a polite way to say, "no?"',
        'Oh, Scott, that hurts daddy when you say that. Honestly.',
        'Let me tell you a little story about a man named SHH! SHH! Even before you start, that was a pre-emptive "shh!" Just know that I have a whole bag of "shh!" with your name on it.',
        'Rain check, please.',
        'Let me just check my calendar.... Yea, no. It\'s a no.',
        'But I am le tiirreeed.',
        'Nah, I\'m not feeling well.',
        'Sorry, I\'m leaving for the Peace Corps in an hour.',
        'I\'d really rather not.',
        'No thanks, I\'m driving.',
        'That\'s just not going to work for me. Sorry.',
        'I have a strict, "No deals with the Devil," policy. Sorry.',
        'Does not compute.... EEEEEEEEE',
        'That idea is not compatible with myself.',
        'I believe there\'s someone a lot more stupid who would enjoy doing that instead.',
        'I shall not.',
        'Here\'s a thought; do it yourself.',
        'If I were genie and could grant you three wishes, I still wouldn\'t do that for you.',
        'My father was a relentlessly self-improving boulangerie owner from Belgium with low-grade narcolepsy and a penchant for buggery. My mother was a 15-year-old French prostitute named Chloe, with webbed feet. My father would womanize, he would drink. He would make outrageous claims like he invented the question mark. Sometimes he would accuse chestnuts of being lazy. The sort of general malaise that only the genius possess and the insane lament. My childhood was typical. Summers in Rangoon, luge lessons. In the spring, we\'d make meat helmets. When I was insolent, I was placed in a burlap bag and beaten with reeds. Pretty standard really. At the age of 12, I received my first scribe. At the age of 14, a Zoroastrian named Vilma ritualistically shaved my testicles. There really is nothing like a shorn scrotum. It\'s breathtaking. I suggest you try it.',
        'Throw me a frickin\' bone here!',
        'Ugh, do I have to?',
        'How about no?',
        'Do I look like your mother?',
        'Some peoples children...'
    ]

quotes = [
          'Thank you, ladies and gentlemen, for tuning us in today. Until next time, I\'m Alex TreBOT, and I hope to see you soon, on Jeopardy!',
          'The answer is...',
          'Here is the clue...',
          'We have some bad news for you...',
          'Take your job seriously, but don\'t take yourself too seriously.',
          'If you can\'t be in awe of Mother Nature, there\'s something wrong with you.',
          'Don\'t tell me what you believe in. I\'ll observe how you behave and I will make my own dtermination.',
          'It\'s very important in life to know when to shut up. You should not be afraid of silence.',
          'I\m curious about everything. Even subjects that don\'t interest me.',
          'My life has been a quest of knowledge and understanding, and I am nowhere near having achieved that. And it doesn\'t bother me in the least. I will die without having come up with answers to many things in life.',
          'I think what makes "Jeopardy!" special is that, among all the quiz and game shows out there, ours tends to encourage learning.',
          'We are all experts in our own little niches.',
          'My life is what it is, and I can\'t change it. I can change the future, but I can\'t do anything about the past.',
          'I don\'t gamble, because winning a hundred dollars doesn\'t give me great pleasure. But losing a hundred dollars pisses me off.',
          'Don\'t minimize the importance for luck in determining life\'s course.',
          'Learning something new is fun.',
          'I don\'t spend any time whatsoever thinking about what might have been.',
          'You should never wear a baseball cap when working in close quarters in the attic: You never see that beam above you!',
          'When you\'re in your 30s and actively pursuing a career and a home life, a wife and children, you\'re busy doing as opposed to busy thinking. As you get older, even as you don\'t have as much time, I think you tend to think more and reflect more on what is happening in your own life.',
          'The only reason I got into broadcasting was, I needed money to pay for my junior and senior years at college, and they hired me, those fools!',
          'Sex? Unfortunately, as you get older - and I shouldn\'t admit this - there are other things that become more important in your daily life.',
          'My heart seems to heal, so that speaks well for my future.',
          'My musical development stopped when Frank Sinatra died.',
          'When I finish as the host of "Jeopardy!" I\'m going to go up to Taft in central California. They have a small college there that teaches you about oil drilling.',
          'I believe the "Jeopardy!" test is more difficult than being a contestant on the program.',
          'I go through these cycles where I read a lot and then watch TV a lot.',
          'I have an Apple computer, which I use to play Spider Solitaire and do research on the internet.',
          'Maybe I\'ll take a little better care of myself, but I wouldn\'t count on it.',
          '"Music Hop" in 1963 was my first hosting job of a variety program.',
          'People say, "You look to be in great shape for your age," and I guess I am. - R.I.P!',
          'I did everything - I did newscasts, I did sports, I did dramas.',
          'I would have loved to have a role in the HBO series "Deadwood." It was Shakespeare in the Old West.',
]

teams = "Fuck, Dutch Air Fryer, The Eastgarths, Quizzards of the Coast, Home Owners & Morgan. J Lo, and Ghibli.\n"

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(f'{client.user} is connected to the following guild:\n'
    f'{guild}(id: {guild.id})')
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author.id == 152203564658327561:
        await message.channel.send('Cheaters don\'t get to talk in my house.')
        return
    else:
        return

@client.command()
@commands.has_role("Admin")
async def timer(ctx):
    guild = discord.utils.get(client.guilds, name=GUILD)
    channel = ctx.author.voice.channel
    await ctx.send("Two minutes, on the clock")
    time.sleep(120)
    count = len(mover)
    tick = 0
    while tick != count:
        tag = mover[tick]
        tick = tick + 1
        try:
            member = guild.get_member(tag)
            await member.move_to(channel)
        except:
            tag = mover[tick]
            tick = tick + 1
            try:
                member = guild.get_member(tag)
                await member.move_to(channel)
            except:
                tag = mover[tick]
                tick = tick + 1
    else:
        await ctx.send("Let's reveal our answers! Good luck.")
            
@client.command()
@commands.has_role("Admin")
async def start(ctx):
    await ctx.send("Now, entering the studio are today's contestants:")
    await ctx.send(teams)
    await ctx.send("These contestants will compete today, on… Trivia Night! And now, here is the host of Trivia Night! Cassidy!\n")
    
@client.command()
async def summon(ctx):
    try:
        channel = ctx.author.voice.channel
        await channel.connect()
        return
    except:
        sassy = random.choice(nope)
        await ctx.send(sassy)
        return
        
@client.command()
async def banish(ctx):
    try:
        await ctx.voice_client.disconnect()
        return
    except:
        sassy = random.choice(nope)
        await ctx.send(sassy)
        return

@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        sassy = random.choice(nope)
        await ctx.send(sassy)
        return

@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        sassy = random.choice(nope)
        await ctx.send(sassy)
        return
    else:
        voice.resume()
        return   

@client.command()
async def play(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    url = 'https://www.youtube.com/watch?v=C59LscG6xxs'
    if not voice.is_playing():
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send("I'm playing the song of my people")
    else:
        sassy = random.choice(fourohfour)
        await ctx.send(sassy)
        return

@client.command()
async def commands(ctx):
    await ctx.author.send('This is Alex TreBOT, and here\'s what I can do:\n'
                          '*start - allow me to announce the show for you.\n'
                          '*timer - starts a 2 minute timer, and then autimatically pulls all users back into your voice channel.\n'
                          '*summon - brings me into your voice channel. (This is NOT required for the timer function.)\n'
                          '*banish - takes me out of your voice channel.\n'
                          '*play - starts a ten hour loop of Jeapordy! music.\n'
                          '*pause - stops playing music.\n'
                          '*resume - continues playing music.\n'
                          '*quote - if you want me to say one of my famous lines.\n')

@client.command()
async def temp(ctx):
    channel = client.get_channel()
    await channel.send('This is Alex TreBOT, and here\'s what I can do:\n',
                       '*start - allow me to announce the show for you.\n',
                       '*timer - starts a 2 minute timer, and then autimatically pulls all users back into your voice channel.\n',
                       '*summon - brings me into your voice channel. (This is NOT required for the timer function.)\n',
                       '*banish - takes me out of your voice channel.\n',
                       '*play - starts a ten hour loop of Jeapordy! music.\n',
                       '*pause - stops playing music.\n',
                       '*resume - continues playing music.\n',
                       '*quote - if you want me to say one of my famous lines.\n'
                       '*commands - if you want me to send this message directly to your DMs.\n')

@client.command()
async def quote(ctx):
    response = random.choice(quotes)
    await ctx.send(response)

client.run(TOKEN)
