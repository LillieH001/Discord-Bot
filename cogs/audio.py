import discord, datetime, asyncio, string, random
from discord.commands import Option, slash_command
from discord.ext import commands
from yt_dlp import YoutubeDL
from gtts import gTTS

class audio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    queue = []

    def is_connected(self, ctx):
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        return voice_client and voice_client.is_connected()

    def is_playing(self, ctx):
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        return voice_client and voice_client.is_playing()

    def youtube_ytdlp(self, video):
        YTDL_OPTIONS = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'ytsearch',
            'no-cache-dir': True,
        }
        with YoutubeDL(YTDL_OPTIONS) as ytdl:
            try:
                info = ytdl.extract_info(video, download=True)['entries'][0]
            except:
                info = ytdl.extract_info(video, download=True)
        return info['title'], info['url']

    def soundcloud_ytdlp(self, video):
        YTDL_OPTIONS = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'scsearch',
            'no-cache-dir': True,
        }
        with YoutubeDL(YTDL_OPTIONS) as ytdl:
            try:
                info = ytdl.extract_info(video, download=True)['entries'][0]
            except:
                info = ytdl.extract_info(video, download=True)
        return info['title'], info['url']

    def other_ytdlp(self, video):
        YTDL_OPTIONS = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'none',
            'no-cache-dir': True,
        }
        with YoutubeDL(YTDL_OPTIONS) as ytdl:
            info = ytdl.extract_info(video, download=True)
        return info['title'], info['url']

    async def voice_player(self, ctx):
        if self.queue:
            tts = gTTS(text=f"Now Playing {self.queue[0]}", lang="en", slow=False)
            filename = ''.join(random.choice(string.ascii_lowercase) for i in range(30))
            tts.save(f"voice/{filename}.mp3")
            source = await discord.FFmpegOpusAudio.from_probe(f"voice/{filename}.mp3")
            ctx.channel.guild.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.audio_player(ctx), self.bot.loop))
        
    async def audio_player(self, ctx):
        if self.queue:
            FFMPEG_OPTIONS = {
                'before_options': '-nostdin -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn',
            }
            source = await discord.FFmpegOpusAudio.from_probe(self.queue[1], **FFMPEG_OPTIONS)
            ctx.channel.guild.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.voice_player(ctx), self.bot.loop))
            del self.queue[:2]
    
    @slash_command(description="Connects the bot to the voice channel you are in")
    async def connect(self, ctx):
        await ctx.defer()
        if ctx.author.voice != None and not self.is_connected(ctx):
            await ctx.author.voice.channel.connect()
            embed = discord.Embed(title="Connected To:", description=ctx.author.voice.channel, color=0xFFC0DD)
            # embed.add_field(name="Connected To:", value=ctx.author.voice.channel, inline=False)
            embed.timestamp = datetime.datetime.now()
            await ctx.send_followup(embed=embed)
        elif ctx.author.voice == None:
            embed = discord.Embed(title="Notice", description="You cannot run voice commands unless you are in the voice channel with the bot", color=0xFFC0DD)
            embed.timestamp = datetime.datetime.now()
            await ctx.send_followup(embed=embed)

    # Music Commands
    
    @slash_command(description="Plays a song")
    async def play(self, ctx, source: Option(str, "Choose audio source", choices=["YouTube", "SoundCloud", "Audiomack", "Bandcamp"]), video: Option(str, "Enter video name or url")):
        if ctx.author.voice != None:
            if not self.is_connected(ctx):
                await self.connect(self, ctx)
            else:
                await ctx.defer()
            if source == "YouTube":
                name, url = self.youtube_ytdlp(video)
            if source == "SoundCloud":
                name, url = self.soundcloud_ytdlp(video)
            if source == "Audiomack" or source == "Bandcamp":
                name, url = self.other_ytdlp(video)
            self.queue.append(name)
            self.queue.append(url)
            embed = discord.Embed(title="Music Player", color=0xFFC0DD)
            embed.add_field(name="Added To Queue:", value=name, inline=False)
            embed.timestamp = datetime.datetime.now()
            await ctx.send_followup(embed=embed)
            if not self.is_playing(ctx):
                # await self.audio_player(ctx)
                await self.voice_player(ctx)
        elif ctx.author.voice == None:
            await ctx.defer()
            embed = discord.Embed(title="Music Player", description="You cannot run voice commands unless you are in the voice channel with the bot", color=0xFFC0DD)
            embed.timestamp = datetime.datetime.now()
            await ctx.send_followup(embed=embed)

    @slash_command(description="Skips to the next song in the queue")
    async def skip(self, ctx):
        await ctx.defer()
        if ctx.author.voice != None and self.is_connected(ctx):
            ctx.channel.guild.voice_client.stop()
            embed = discord.Embed(title="Music Player", color=0xFFC0DD)
            embed.add_field(name="Skipped Playing Song In:", value=ctx.author.voice.channel, inline=False)
            embed.timestamp = datetime.datetime.now()
            await ctx.send_followup(embed=embed)
            await self.audio_player(ctx)
        elif ctx.author.voice == None:
            embed = discord.Embed(title="Music Player", description="You cannot run voice commands unless you are in the voice channel with the bot", color=0xFFC0DD)
            embed.timestamp = datetime.datetime.now()
            await ctx.send_followup(embed=embed)
        elif not self.is_connected(ctx):
            embed = discord.Embed(title="Music Player", description="I am not connected to any voice channel", color=0xFFC0DD)
            embed.timestamp = datetime.datetime.now()
            await ctx.send_followup(embed=embed)
            
    @slash_command(description="Stops and disconnects the bot")
    async def stop(self, ctx):
        await ctx.defer()
        if ctx.author.voice != None and self.is_connected(ctx):
            self.queue.clear()
            ctx.channel.guild.voice_client.stop()
            await ctx.channel.guild.voice_client.disconnect()
            embed = discord.Embed(title="Music Player", color=0xFFC0DD)
            embed.add_field(name="Stopped Playing In:", value=ctx.author.voice.channel, inline=False)
            embed.timestamp = datetime.datetime.now()
            await ctx.send_followup(embed=embed)
        elif ctx.author.voice == None:
            embed = discord.Embed(title="Music Player", description="You cannot run voice commands unless you are in the voice channel with the bot", color=0xFFC0DD)
            embed.timestamp = datetime.datetime.now()
            await ctx.send_followup(embed=embed)
        elif not self.is_connected(ctx):
            embed = discord.Embed(title="Music Player", description="I am not connected to any voice channel", color=0xFFC0DD)
            embed.timestamp = datetime.datetime.now()
            await ctx.send_followup(embed=embed)

    @slash_command(description="Pauses the playing song")
    async def pause(self, ctx):
        await ctx.defer()
        if ctx.author.voice != None and self.is_connected(ctx):
            if self.is_playing(ctx):
                ctx.channel.guild.voice_client.pause()
                embed = discord.Embed(title="Music Player", color=0xFFC0DD)
                embed.add_field(name="Paused Playing In:", value=ctx.author.voice.channel, inline=False)
                embed.timestamp = datetime.datetime.now()
                await ctx.send_followup(embed=embed)
            else:
                embed = discord.Embed(title="Music Player", description="I am currently not playing anything", color=0xFFC0DD)
                embed.timestamp = datetime.datetime.now()
                await ctx.send_followup(embed=embed)
        elif ctx.author.voice == None:
            embed = discord.Embed(title="Music Player", description="You cannot run voice commands unless you are in the voice channel with the bot", color=0xFFC0DD)
            embed.timestamp = datetime.datetime.now()
            await ctx.send_followup(embed=embed)
        elif not self.is_connected(ctx):
            embed = discord.Embed(title="Music Player", description="I am not connected to any voice channel", color=0xFFC0DD)
            embed.timestamp = datetime.datetime.now()
            await ctx.send_followup(embed=embed)

    @slash_command(description="Resumes the playing song")
    async def resume(self, ctx):
        await ctx.defer()
        if ctx.author.voice != None and self.is_connected(ctx):
            if not self.is_playing(ctx):
                ctx.channel.guild.voice_client.resume()
                embed = discord.Embed(title="Music Player", color=0xFFC0DD)
                embed.add_field(name="Resumed Playing In:", value=ctx.author.voice.channel, inline=False)
                embed.timestamp = datetime.datetime.now()
                await ctx.send_followup(embed=embed)
            else:
                embed = discord.Embed(title="Music Player", description="I am currently not paused", color=0xFFC0DD)
                embed.timestamp = datetime.datetime.now()
                await ctx.send_followup(embed=embed)
        elif ctx.author.voice == None:
            embed = discord.Embed(title="Music Player", description="You cannot run voice commands unless you are in the voice channel with the bot", color=0xFFC0DD)
            embed.timestamp = datetime.datetime.now()
            await ctx.send_followup(embed=embed)
        elif not self.is_connected(ctx):
            embed = discord.Embed(title="Music Player", description="I am not connected to any voice channel", color=0xFFC0DD)
            embed.timestamp = datetime.datetime.now()
            await ctx.send_followup(embed=embed)

    # Text To Speech Commands

    @slash_command(description="Text to speech")
    async def tts(self, ctx, text: Option(str, "Enter text to speak")):
        if ctx.author.voice != None:
            if not self.is_connected(ctx):
                await self.connect(self, ctx)
            else:
                await ctx.defer()
                if not self.queue:
                    texttospeech = gTTS(text=text, lang="en", slow=False)
                    filename = ''.join(random.choice(string.ascii_lowercase) for i in range(30))
                    texttospeech.save(f"texttospeech/{filename}.mp3")
                    source = await discord.FFmpegOpusAudio.from_probe(f"texttospeech/{filename}.mp3")
                    ctx.channel.guild.voice_client.play(source)
                    await ctx.send_followup(f"This is a test")
        elif ctx.author.voice == None:
            await ctx.defer()
            embed = discord.Embed(title="Text To Speech", description="You cannot run voice commands unless you are in the voice channel with the bot", color=0xFFC0DD)
            embed.timestamp = datetime.datetime.now()
            await ctx.send_followup(embed=embed)

def setup(bot):
    bot.add_cog(audio(bot))