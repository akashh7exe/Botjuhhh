import discord
from discord.ext import commands
import os 
from dotenv import load_dotenv
from Help_cog import help_cog
import music_cog
import pathlib
from pathlib import Path
from discord import Intents


load_dotenv()


intents = discord.Intents.default()
intents.message_content = True
intents.members = True


bot =  commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def LOL(ctx):
    await ctx.send('LOl is Lol')


@bot.command()
async def calc(ctx, arg1: int, arg2: int):
    try:
        answ = arg1 + arg2
        await ctx.send(answ)
    except Exception:
        await ctx.send("Are you sure those are two numbers?")


@bot.command()
async def Boss(ctx):
    if ctx.author.id == 426007433840689152:
        await ctx.send('This is the Owner')
 

@bot.command()
async def Hoi(ctx):
    await ctx.send('Hey hoe is het?')

@bot.command()
async def ping(ctx):
    await ctx.send("pong!")


@bot.command()
async def funfact (ctx): 
    await ctx.send("The Eiffel Tower can be 15 cm taller during the summer, due to thermal expansion meaning the iron heats up, the particles gain kinetic energy and take up more space.")

@bot.command()
async def moe (ctx):
    await ctx.send("slapen is een goed idee om te doen")

async def main():
    await bot.load_extension('music_cog')
  

             
  

bot.run(os.getenv("token"))