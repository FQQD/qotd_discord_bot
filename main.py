import os, disnake, random, re
import disnake.ext
from disnake.ext import tasks
from disnake.ext import commands
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path

load_dotenv()
TOKEN = 'YOUR_TOKEN'


client = commands.Bot(
    command_prefix=disnake.ext.commands.when_mentioned,
    activity=disnake.Activity(type=disnake.ActivityType.watching, name="made by FQQD.ᴅᴇ")
)

#ID of channel where questions are posted
target = YOUR_CHANNEL #fill in

#Hour QOTD is to be posted
posttime = YOUR_POSTTIME #fill in

embedcolor = disnake.Colour.green()

errorembedcolor = disnake.Colour.red()

questionsfile = Path(__file__).with_name('questions.txt')
tempfile = Path(__file__).with_name('temp.txt')

#Adds a question to the text file when called.
def question_add(question):
    with open(questionsfile, 'a') as questions:
        questions.write(question+'\n')

def remove_question(qotd):
    with open (questionsfile, "r") as input:
        with open (tempfile, "w") as output:
            for line in input:
                if line.strip("\n") != qotd:
                    output.write(line)
    os.replace(tempfile, questionsfile)

#Posts question of the day when called.
async def question_post(channel):
    with open(questionsfile, 'r') as questions:
        qlines = questions.read().splitlines()
        try:
            qotd = random.choice(qlines)
            embed = disnake.Embed(
                title = f"{qotd}",
                description = f"Post your answers in the Thread down below!",
                colour = embedcolor,
            )
            embed.set_author(name=f"Question Of The Day:", icon_url='https://imgur.com/iGasyeb.png')
            embed.set_footer(text=f"Do you also submit a question? Use /add.")
            await channel.send(embed=embed)
            
            message = channel.last_message
            await message.create_thread(
                name=f"'{qotd}'",
                auto_archive_duration=60,
            )
        
            remove_question(qotd)
            
        except:
            embed = disnake.Embed(
                title = f"QOTD: No questions left.",
                description = f"Everyone submit one, using **/add**!",
                colour = errorembedcolor,
            )
            await channel.send(embed=embed)
    print(f'{client.user} has posted a qotd!')

#Scheduled to call question of the day.
@tasks.loop(minutes=60)
async def task():
    if datetime.now().hour == posttime:
        channel = client.get_channel(target)
        await question_post(channel)

#Make sure bot is online.
@client.event
async def on_ready():
    print(f'{client.user} has connected to disnake! It is '+ str(datetime.now()))
    await task.start()

#Reads for commands, which includes adding questions and testing
        
@client.slash_command(name="add", description="Add QOTD")
async def add(inter, question):
    embed = disnake.Embed(
        title = f"Added QOTD! Thank you for submitting.",
        description = f"'{question}'",
        colour = embedcolor,
    )
    await inter.send(embed=embed)
    question_add(question)
    print(f'{inter.author} has added "{question}"!')
    
@client.slash_command(name="test", description="Tests QOTD")
@commands.has_permissions(kick_members=True)
async def test(inter):
    channel = client.get_channel(target)
    await question_post(channel)
    embed = disnake.Embed(
        title = f"Success!",
        description = f"Sent a QOTD.",
        colour = embedcolor,
    )
    await inter.send(embed=embed)

@client.slash_command(name="say", description="Send a dummy message")
@commands.has_permissions(kick_members=True)
async def say(inter, question):
    channel = client.get_channel(target)
    await channel.send(question)
    embed = disnake.Embed(
        title = f"Success!",
        description = f"Sent the message.",
        colour = embedcolor,
    )
    await inter.send(embed=embed)

client.run(TOKEN)
