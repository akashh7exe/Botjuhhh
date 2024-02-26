from winreg import QueryValue
import discord
from discord.ext import commands
from ast import alias
from yt_dlp import YoutubeDL
import asyncio
from youtube_dl import YoutubeDL
from youtube_dl.utils import args_to_str


  
class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        #all the music related stuff
        self.is_playing = False
        self.is_paused = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS ={ 'format': 'bestaudio' , 'noplaylist': 'true'}
        self.FFMPEG_OPTIONS = {'before_options' : 'reconnect 1 -reconnect_streamd 1 -reconnect_delay_max 5' , 'options': '-vn'}

        self.vc = None

def search_yt(self,item):
  with YoutubeDL(self.YDL_OPTIONS) as ydl:
    try:
       info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'[0]]
    except Exception:
          return False
  return {'source': info['formats'[0][0]], 'title': info['title']}

def play_next(self): 
    if len(self.music_queue) >0: 
        self.is_playing = True
        
        m_url = self.music_queue[0][0]['source']
        
        self.music_queue.pop(0)
        
        self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS) )
    else:
        self.is_playing = False

async def play_music(self, ctx):
     if len(self.music_queue) >0: 
        self.is_playing = True
        m_url = self.music_queue[0][0]['source']

        if self.vc == None:
            await ctx.send("Could not connect to voice channel")
            return  
        else:
            await self.vc.move_to(self.music_queue[0][1])

        self.music_queue.pop(0) 
        
        self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTOIONS), after=lambda e: self.play_next())

        @commands.command(name="play", aliase=["p, playing"] ,help='play the selected song from Youtube')
        async def play(self, ctx, *agrs):
            query =" ".join(*args_to_str)  

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("connect to a voice channel")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(QueryValue)
            if type(song) == type(True):
                await ctx.send("```Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.```")
            else:
                if self.is_playing:
                    await ctx.send(f"**#{len(self.music_queue)+2} -'{song['title']}'** added to the queue")  
                else:
                    await ctx.send(f"**'{song['title']}'** added to the queue")  
                self.music_queue.append([song, voice_channel])
                if self.is_playing == False:
                    await self.play_music(ctx)

@commands.command(name = "resume", aliases=["r"], help="Resumes playing with the discord bot")
async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

@commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            #try to play next in the queue if it exists
            await self.play_music(ctx)
@commands.command(name="queue", aliases=["q"], help="Displays the current songs in queue")
async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += f"#{i+1} -" + self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(f"```queue:\n{retval}```")
        else:
            await ctx.send("```No music in queue```")        
@commands.command(name="clear", aliases=["c", "bin"], help="Stops the music and clears the queue")
async def clear(self, ctx):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("```Music queue cleared```")

@commands.command(name="stop", aliases=["disconnect", "l", "d"], help="Kick the bot from VC")
async def dc(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()
@commands.command(name="remove", help="Removes last song added to queue")
async def re(self, ctx):
        self.music_queue.pop()
        await ctx.send("```last song removed```")


